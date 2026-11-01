const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

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
  const cleanStr = sent.replace(/[.,!?;:()„“”"'/]/g, ' ');
  const tokens = cleanStr.split(/\s+/).filter(Boolean);
  for (const tok of tokens) {
    if (/^[A-Za-zÄÖÜäöüß]+$/.test(tok)) {
      words.add(tok);
    }
  }
}

// Canonical casing map: lowercase -> best casing
const canonicalMap = new Map();
for (const w of words) {
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

async function fetchAudio(casedWord) {
  const capitalized = casedWord.charAt(0).toUpperCase() + casedWord.slice(1);
  const lower = casedWord.toLowerCase();
  const cands = Array.from(new Set([casedWord, capitalized, lower]));

  // 1. Try Wikimedia Commons MP3
  for (const cand of cands) {
    const fn = `De-${cand}.ogg`;
    const url = getWikimediaMp3Url(fn);
    try {
      const res = await fetch(url, {
        headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' },
        signal: AbortSignal.timeout(4000),
      });
      if (res.status === 200) {
        const buf = Buffer.from(await res.arrayBuffer());
        if (buf.length > 500) {
          return { source: 'wikimedia', buf };
        }
      }
    } catch {
      // ignore
    }
  }

  // 2. Fall back to Google Translate TTS MP3 (high-fidelity neural German voice)
  const googleUrl = `https://translate.google.com/translate_tts?ie=UTF-8&tl=de&client=tw-ob&q=${encodeURIComponent(casedWord)}`;
  try {
    const gRes = await fetch(googleUrl, {
      headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' },
      signal: AbortSignal.timeout(4000),
    });
    if (gRes.status === 200) {
      const buf = Buffer.from(await gRes.arrayBuffer());
      if (buf.length > 500) {
        return { source: 'google', buf };
      }
    }
  } catch {
    // ignore
  }

  return null;
}

const outDir = path.resolve('public/audio/words');
if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

async function main() {
  const entries = Array.from(canonicalMap.entries());
  console.log(`Processing ${entries.length} words...`);

  const manifest = {};
  let wikiCount = 0;
  let googleCount = 0;
  let skippedCount = 0;
  let failedCount = 0;

  // Concurrency pool of 6
  const CONCURRENCY = 6;
  let index = 0;

  async function worker(_workerId) {
    while (index < entries.length) {
      const currentIndex = index++;
      const [lower, cased] = entries[currentIndex];
      const slug = toAsciiSlug(lower);
      const filePath = path.join(outDir, `${slug}.mp3`);
      const publicPath = `/audio/words/${slug}.mp3`;

      manifest[lower] = publicPath;

      if (fs.existsSync(filePath) && fs.statSync(filePath).size > 500) {
        skippedCount++;
        continue;
      }

      const result = await fetchAudio(cased);
      if (result) {
        fs.writeFileSync(filePath, result.buf);
        if (result.source === 'wikimedia') wikiCount++;
        else googleCount++;
      } else {
        console.warn(`[FAIL] ${cased} (${lower})`);
        failedCount++;
      }

      if ((currentIndex + 1) % 50 === 0 || currentIndex + 1 === entries.length) {
        console.log(`Progress: ${currentIndex + 1}/${entries.length} (Wiki: ${wikiCount}, Google: ${googleCount}, Skipped: ${skippedCount}, Failed: ${failedCount})`);
      }
      // Small breather
      await new Promise(r => setTimeout(r, 60));
    }
  }

  const workers = [];
  for (let i = 0; i < CONCURRENCY; i++) {
    workers.push(worker(i));
  }
  await Promise.all(workers);

  console.log(`Finished: ${wikiCount} Wikimedia, ${googleCount} Google, ${skippedCount} skipped, ${failedCount} failed.`);

  // Write TypeScript manifest
  const tsContent = `// Auto-generated native German pronunciation audio registry
// Covers all vocabulary and transcript tokens in Hoerlabor listening tracks.

export const BUNDLED_WORD_AUDIO: Record<string, string> = ${JSON.stringify(manifest, null, 2)};
`;
  fs.writeFileSync('src/data/bundledWordAudio.ts', tsContent, 'utf8');
  console.log(`Generated src/data/bundledWordAudio.ts with ${Object.keys(manifest).length} entries.`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
