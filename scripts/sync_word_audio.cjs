const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const OUT_DIR = path.resolve('public/audio/words');
if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

const seed = fs.readFileSync('src/data/seedTracks.ts', 'utf8');
const generated = require('../src/data/generatedTracks.json');

const allSentences = [];
for (const match of seed.matchAll(/german:\s*'([^']+)'/g)) {
  allSentences.push(match[1]);
}
for (const t of generated) {
  for (const s of (t.segments || [])) {
    if (s.german) allSentences.push(s.german);
    for (const v of (s.vocab || [])) {
      if (v.word) allSentences.push(v.word);
    }
  }
}

const words = new Set();
for (const sent of allSentences) {
  const clean = sent
    .replace(/^(der|die|das|sich|den|dem|des|ein|eine)\s+/i, '')
    .replace(/\s*\(\+.*\)/g, '')
    .replace(/[.,!?;:()„“”"'/]/g, ' ');
  const tokens = clean.split(/\s+/).filter(Boolean);
  for (const tok of tokens) {
    if (/^[A-Za-zÄÖÜäöüß]+$/.test(tok)) {
      words.add(tok);
    }
  }
}

const canonicalMap = new Map();
for (const w of Array.from(words).sort()) {
  const lower = w.toLowerCase();
  if (!canonicalMap.has(lower)) {
    canonicalMap.set(lower, w);
  } else {
    const existing = canonicalMap.get(lower);
    if (/^[A-ZÄÖÜ]/.test(w) && !/^[A-ZÄÖÜ]/.test(existing)) {
      canonicalMap.set(lower, w);
    }
  }
}

function toAsciiSlug(word) {
  return word
    .toLowerCase()
    .replace(/ä/g, 'ae')
    .replace(/ö/g, 'oe')
    .replace(/ü/g, 'ue')
    .replace(/ß/g, 'ss')
    .replace(/[^a-z0-9]/g, '_');
}

function getWikimediaMp3Url(filename) {
  const titleForHash = filename.replace(/ /g, '_');
  const hash = crypto.createHash('md5').update(Buffer.from(titleForHash, 'utf8')).digest('hex');
  const h1 = hash[0];
  const h2 = hash.substring(0, 2);
  return `https://upload.wikimedia.org/wikipedia/commons/transcoded/${h1}/${h2}/${encodeURIComponent(titleForHash)}/${encodeURIComponent(titleForHash)}.mp3`;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function fetchFromWikimedia(url) {
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const res = await fetch(url, {
        headers: {
          'User-Agent': 'HoerLabor/2.0 (https://hoerlabor-app.pages.dev; Abc13141580185@gmail.com)'
        },
        signal: AbortSignal.timeout(4000)
      });
      if (res.status === 200) {
        const buf = Buffer.from(await res.arrayBuffer());
        if (buf.length > 1000) return buf;
      } else if (res.status === 429) {
        // Wikimedia 429 backoff
        await sleep(2000 * (attempt + 1));
      } else {
        return null;
      }
    } catch {
      await sleep(1000);
    }
  }
  return null;
}

async function main() {
  const entries = Array.from(canonicalMap.entries());
  console.log(`Checking ${entries.length} canonical words for authentic Wikimedia human recordings...`);

  const slugToCased = new Map();
  for (const [lower, cased] of entries) {
    const slug = toAsciiSlug(lower);
    if (!slugToCased.has(slug)) {
      slugToCased.set(slug, cased);
    } else if (/^[A-ZÄÖÜ]/.test(cased) && !/^[A-ZÄÖÜ]/.test(slugToCased.get(slug))) {
      slugToCased.set(slug, cased);
    }
  }

  const slugItems = Array.from(slugToCased.entries());
  console.log(`Unique audio slugs: ${slugItems.length}`);

  let wikiCount = 0;
  let reusedCount = 0;
  const missingForNeural = [];
  let index = 0;

  async function worker(_workerId) {
    while (index < slugItems.length) {
      const currentIndex = index++;
      const [slug, cased] = slugItems[currentIndex];
      const filePath = path.join(OUT_DIR, `${slug}.mp3`);

      // Reuse existing verified ID3 file
      if (fs.existsSync(filePath) && fs.statSync(filePath).size > 1500) {
        const fd = fs.openSync(filePath, 'r');
        const header = Buffer.alloc(3);
        fs.readSync(fd, header, 0, 3, 0);
        fs.closeSync(fd);
        if (header.toString() === 'ID3') {
          wikiCount++;
          reusedCount++;
          continue;
        }
      }

      const cap = cased.charAt(0).toUpperCase() + cased.slice(1);
      const low = cased.toLowerCase();

      // Batch 1: Primary .ogg (original, cap, low)
      const primaryFiles = Array.from(new Set([`De-${cased}.ogg`, `De-${cap}.ogg`, `De-${low}.ogg`]));
      const batch1Results = await Promise.all(primaryFiles.map(fn => fetchFromWikimedia(getWikimediaMp3Url(fn))));
      let foundBuf = batch1Results.find(b => b && b.length > 1000);

      // Batch 2: Secondary (.oga, .ogg2, De-at) only if Batch 1 missed
      if (!foundBuf) {
        const secondaryFiles = Array.from(new Set([`De-${cap}.oga`, `De-${cased}2.ogg`, `De-${cap}2.ogg`, `De-at-${cap}.ogg`]));
        const batch2Results = await Promise.all(secondaryFiles.map(fn => fetchFromWikimedia(getWikimediaMp3Url(fn))));
        foundBuf = batch2Results.find(b => b && b.length > 1000);
      }

      if (foundBuf) {
        fs.writeFileSync(filePath, foundBuf);
        wikiCount++;
      } else {
        missingForNeural.push({ slug, cased });
      }

      const done = currentIndex + 1;
      if (done % 50 === 0 || done === slugItems.length) {
        console.log(`[${done}/${slugItems.length}] Progress: ${wikiCount} Wikimedia human (reused: ${reusedCount}), ${missingForNeural.length} need Edge Neural`);
      }

      await sleep(120);
    }
  }

  // 3 concurrent workers
  await Promise.all([worker(1), worker(2), worker(3)]);

  console.log(`Wikimedia scan complete! ${wikiCount} human files saved. ${missingForNeural.length} words to be generated by Edge Neural.`);
  fs.writeFileSync('scripts/missing_neural.json', JSON.stringify(missingForNeural, null, 2), 'utf8');

  // Also write manifest
  const manifest = {};
  for (const [lower] of entries) {
    const slug = toAsciiSlug(lower);
    manifest[lower] = `/audio/words/${slug}.mp3`;
  }
  const tsContent = `// Auto-generated native German pronunciation audio registry
// Covers all vocabulary and transcript tokens in Hoerlabor listening tracks.

export const BUNDLED_WORD_AUDIO: Record<string, string> = ${JSON.stringify(manifest, null, 2)};
`;
  fs.writeFileSync('src/data/bundledWordAudio.ts', tsContent, 'utf8');
}

main().catch(console.error);
