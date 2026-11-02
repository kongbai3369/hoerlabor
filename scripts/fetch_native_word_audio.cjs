const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const OUT_DIR = path.resolve('public/audio/words');
if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

// 1. Collect all words from generatedTracks and seedTracks
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

// Canonical casing
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

// Sleep helper
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function fetchWithRetry(url, maxRetries = 2) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const res = await fetch(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 HoerLabor/2.0'
        },
        signal: AbortSignal.timeout(6000)
      });
      if (res.status === 200) {
        const buf = Buffer.from(await res.arrayBuffer());
        if (buf.length > 1000) return buf;
      } else if (res.status === 429) {
        // Rate limited - back off
        await sleep(1500 * (attempt + 1));
      } else {
        // 404 or other status
        return null;
      }
    } catch {
      if (attempt < maxRetries) await sleep(800);
    }
  }
  return null;
}

// Generate candidate filenames for a word
function getCandidateFilenames(cased) {
  const cap = cased.charAt(0).toUpperCase() + cased.slice(1);
  const low = cased.toLowerCase();
  const cands = Array.from(new Set([cased, cap, low]));

  const files = [];
  for (const c of cands) {
    files.push(`De-${c}.ogg`);
    files.push(`De-${c}2.ogg`);
    files.push(`De-${c}.oga`);
    files.push(`De-at-${c}.ogg`);
  }

  // Lemma fallbacks for inflected verbs/adjectives
  // e.g. mache -> machen, gemacht -> machen, groesser -> gross
  const lemmas = [];
  if (low.endsWith('e') && low.length > 3) lemmas.push(low + 'n');
  if (low.endsWith('t') && low.length > 4) lemmas.push(low.slice(0, -1) + 'en');
  if (low.endsWith('st') && low.length > 4) lemmas.push(low.slice(0, -2) + 'en');
  if (low.endsWith('te') && low.length > 4) lemmas.push(low.slice(0, -2) + 'en');
  if (low.endsWith('ten') && low.length > 5) lemmas.push(low.slice(0, -3) + 'en');
  if (low.endsWith('em') && low.length > 4) lemmas.push(low.slice(0, -2));
  if (low.endsWith('en') && low.length > 4) lemmas.push(low.slice(0, -2));
  if (low.endsWith('er') && low.length > 4) lemmas.push(low.slice(0, -2));
  if (low.endsWith('es') && low.length > 4) lemmas.push(low.slice(0, -2));

  for (const l of lemmas) {
    const lCap = l.charAt(0).toUpperCase() + l.slice(1);
    files.push(`De-${l}.ogg`);
    files.push(`De-${lCap}.ogg`);
    files.push(`De-${l}.oga`);
  }

  return Array.from(new Set(files));
}

async function main() {
  const entries = Array.from(canonicalMap.entries());
  console.log(`Processing ${entries.length} words...`);

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
  let fallbackCount = 0;

  for (let i = 0; i < slugItems.length; i++) {
    const [slug, cased] = slugItems[i];
    const filePath = path.join(OUT_DIR, `${slug}.mp3`);

    // Check if already authentic Wikimedia audio (ID3 header + size > 1500)
    if (fs.existsSync(filePath) && fs.statSync(filePath).size > 1500) {
      const fd = fs.openSync(filePath, 'r');
      const headerBuf = Buffer.alloc(3);
      fs.readSync(fd, headerBuf, 0, 3, 0);
      fs.closeSync(fd);
      if (headerBuf.toString() === 'ID3') {
        reusedCount++;
        wikiCount++;
        continue;
      }
    }

    const candidateFiles = getCandidateFilenames(cased);
    let found = false;

    for (const fn of candidateFiles) {
      const url = getWikimediaMp3Url(fn);
      const buf = await fetchWithRetry(url);
      if (buf) {
        fs.writeFileSync(filePath, buf);
        wikiCount++;
        found = true;
        break;
      }
      // Polite delay between candidate checks to avoid 429
      await sleep(150);
    }

    if (!found) {
      fallbackCount++;
      // If we don't have a human Wikimedia recording, keep the existing file or note it
    }

    if ((i + 1) % 25 === 0 || i + 1 === slugItems.length) {
      console.log(`Progress: ${i + 1}/${slugItems.length} (Human Wiki: ${wikiCount}, Reused: ${reusedCount}, Fallback: ${fallbackCount})`);
    }

    // Polite delay between words
    await sleep(400);
  }

  console.log(`Finished: ${wikiCount} Human Wikimedia recordings (${reusedCount} reused), ${fallbackCount} fallbacks.`);

  // Write TypeScript registry
  const manifest = {};
  for (const [lower] of entries) {
    const slug = toAsciiSlug(lower);
    manifest[lower] = `/audio/words/${slug}.mp3`;
  }

  const tsContent = `// Auto-generated native German pronunciation audio registry
// Covers all vocabulary and transcript tokens in Hoerlabor listening tracks.
// Audio files are prioritized for 100% native human recordings (Wikimedia Commons).

export const BUNDLED_WORD_AUDIO: Record<string, string> = ${JSON.stringify(manifest, null, 2)};
`;

  fs.writeFileSync('src/data/bundledWordAudio.ts', tsContent, 'utf8');
  console.log(`Updated src/data/bundledWordAudio.ts with ${Object.keys(manifest).length} entries.`);
}

main().catch(console.error);
