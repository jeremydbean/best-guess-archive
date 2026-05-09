import fs from 'node:fs';
import vm from 'node:vm';

const asJson = process.argv.includes('--json');
const shouldFix = process.argv.includes('--fix');
const expectedSections = ['Intro', 'Round 1', 'Round 1 Results', 'Round 2', 'Round 2 Results', 'Outro'];
const readJson = path => JSON.parse(fs.readFileSync(path, 'utf8'));
const writeJson = (path, value) => fs.writeFileSync(path, `${JSON.stringify(value, null, 2)}\n`);
const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const weekdayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const datePattern = new RegExp(`^(${weekdayNames.join('|')}), (${monthNames.join('|')}) (\\d{1,2}), (\\d{4})$`);
const loose = value => String(value || '')
  .normalize('NFKD')
  .replace(/[’']/g, '')
  .replace(/&/g, 'AND')
  .replace(/[^A-Z0-9]+/gi, '')
  .toUpperCase();

// Load games from year shards; fall back to games.json if shards are absent.
const yearShardFiles = fs.readdirSync('data').filter(f => /^games-\d{4}\.json$/.test(f)).sort();
let games;
if (yearShardFiles.length > 0) {
  games = yearShardFiles.flatMap(f => readJson(`data/${f}`));
} else {
  games = readJson('data/games.json');
}

let metaRaw = readJson('data/games-meta.json');
// Support both old bare-array format and new {years, games} object format.
let meta = Array.isArray(metaRaw) ? metaRaw : (metaRaw.games || []);
const transcripts = readJson('data/transcripts.json');
const issues = [];
const fixes = [];
const warn = (code, message, context = {}) => issues.push({ level: 'warn', code, message, ...context });
const error = (code, message, context = {}) => issues.push({ level: 'error', code, message, ...context });

function validateArchiveDate(date, context = {}) {
  const match = String(date || '').match(datePattern);
  if (!match) {
    error('date-format', 'Date must use "Weekday, Month D, YYYY" format', { date, ...context });
    return;
  }
  const [, weekday, month, dayRaw, yearRaw] = match;
  const monthIndex = monthNames.indexOf(month);
  const day = Number(dayRaw);
  const year = Number(yearRaw);
  const actual = new Date(year, monthIndex, day);
  const isValidDate = actual.getFullYear() === year && actual.getMonth() === monthIndex && actual.getDate() === day;
  if (!isValidDate) {
    error('date-value', 'Date is not a valid calendar day', { date, ...context });
    return;
  }
  const expectedWeekday = weekdayNames[actual.getDay()];
  if (weekday !== expectedWeekday) {
    error('date-weekday', `Date weekday should be ${expectedWeekday}`, { date, ...context });
  }
}

function archiveDateValue(date) {
  const match = String(date || '').match(datePattern);
  if (!match) return 0;
  const [, , month, dayRaw, yearRaw] = match;
  return (Number(yearRaw) * 10000) + ((monthNames.indexOf(month) + 1) * 100) + Number(dayRaw);
}

function validatePayoutValue(value, field, context = {}) {
  if (value == null || value === '') return;
  const numeric = Number(String(value).replace(/[$,]/g, ''));
  if (!Number.isFinite(numeric) || numeric < 0) {
    error('payout-value', 'Payout field must be a non-negative number', { field, value, ...context });
  }
}

function parseCountValue(value) {
  if (value == null || value === '') return NaN;
  const digits = String(value).replace(/[^\d]/g, '');
  return digits ? Number(digits) : NaN;
}

function validateCountValue(value, field, context = {}, options = {}) {
  if (value == null || value === '') return NaN;
  if (options.allowLegacyUnknown && /^(?:N|N\/A|A \/ N\/A|\?|-)$/.test(String(value).trim())) return NaN;
  const numeric = parseCountValue(value);
  if (!Number.isInteger(numeric) || numeric < 0) {
    error('count-value', 'Count field must be a non-negative integer', { field, value, ...context });
  }
  return numeric;
}

const floorCents = value => Math.floor(Number(value || 0) * 100) / 100;
const moneyMatches = (actual, expected) => Math.abs(Number(actual || 0) - Number(expected || 0)) < 0.005;

function expectedV2Payouts(game) {
  const goldWinners = Number(game.goldWinners || 0);
  const silverWinners = Number(game.silverWinners || 0);
  const bronzeWinners = Number(game.bronzeWinners || 0);
  let bronzeShare = 0;
  let silverShare = 0;

  if (bronzeWinners === 0) {
    const bronzeRecipients = silverWinners === 0 ? goldWinners : goldWinners + silverWinners;
    if (bronzeRecipients > 0) bronzeShare = floorCents(2000 / bronzeRecipients);
  }
  if (silverWinners === 0 && goldWinners > 0) {
    silverShare = floorCents(2500 / goldWinners);
  }

  return {
    goldPayout: goldWinners > 0 ? Number((floorCents(3000 / goldWinners) + bronzeShare + silverShare).toFixed(2)) : 0,
    silverPayout: silverWinners > 0 ? Number((floorCents(2500 / silverWinners) + (bronzeWinners === 0 ? bronzeShare : 0)).toFixed(2)) : 0,
    bronzePayout: bronzeWinners > 0 ? floorCents(2000 / bronzeWinners) : 0
  };
}

const regeneratedMeta = games.map(g => {
  const entry = {
    date: g.date,
    secretItem: g.secretItem,
    pot: g.pot,
    host: g.host ?? null,
    format: g.format,
    totalWinners: g.totalWinners || 0,
    clueCount: (g.clues || []).length
  };
  if (g.goldClue) entry.goldClue = g.goldClue;
  if (g.silverClue) entry.silverClue = g.silverClue;
  if (g.bronzeClue) entry.bronzeClue = g.bronzeClue;
  if (g.note) entry.note = g.note;
  return entry;
});

const years = [...new Set(games.map(g => String(g.date || '').split(' ').pop()))].filter(Boolean).sort();
if (JSON.stringify(regeneratedMeta) !== JSON.stringify(meta)) {
  if (shouldFix) {
    writeJson('data/games-meta.json', { years, games: regeneratedMeta });
    meta = regeneratedMeta;
    fixes.push({ code: 'meta-regenerated', path: 'data/games-meta.json' });
  } else {
    error('meta-mismatch', 'data/games-meta.json is out of sync with year shards. Run `npm run audit:fix` to regenerate it.');
  }
} else if (shouldFix && !Array.isArray(metaRaw) && JSON.stringify(metaRaw.years) !== JSON.stringify(years)) {
  // years array changed (new year shard added) even though games list matched
  writeJson('data/games-meta.json', { years, games: regeneratedMeta });
  fixes.push({ code: 'meta-years-updated', path: 'data/games-meta.json' });
}

const html = fs.readFileSync('index.html', 'utf8');
let inlineScriptCount = 0;
for (const match of html.matchAll(/<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi)) {
  inlineScriptCount += 1;
  try {
    new vm.Script(match[1]);
  } catch (err) {
    error('inline-script-parse', `Inline script ${inlineScriptCount} does not parse`, { detail: err.message });
  }
}

const playableByDate = new Map();
const allDates = new Set();
for (const [index, g] of games.entries()) {
  allDates.add(g.date);
  validateArchiveDate(g.date, { index, source: 'games.json', secretItem: g.secretItem });
  const isStub = !!g.note || (!g.secretItem && (!g.clues || !g.clues.length));
  if (!playableByDate.has(g.date)) playableByDate.set(g.date, []);
  if (!isStub) playableByDate.get(g.date).push(g);

  if (!isStub && (!Array.isArray(g.clues) || g.clues.length !== 5)) {
    error('clue-count', 'Playable game does not have exactly five clues', { index, date: g.date, secretItem: g.secretItem });
  }
  if (!isStub && Array.isArray(g.clues)) {
    g.clues.forEach((clue, clueIndex) => {
      const expectedNumber = clueIndex + 1;
      const clueNumber = validateCountValue(clue.number ?? expectedNumber, 'number', { index, date: g.date, secretItem: g.secretItem, clue: expectedNumber });
      if (clueNumber !== expectedNumber) {
        error('clue-number', 'Playable clue number is out of order', { index, date: g.date, secretItem: g.secretItem, clue: expectedNumber, actual: clue.number });
      }
      validateCountValue(clue.correct, 'correct', { index, date: g.date, secretItem: g.secretItem, clue: expectedNumber }, { allowLegacyUnknown: true });
      validateCountValue(clue.guesses, 'guesses', { index, date: g.date, secretItem: g.secretItem, clue: expectedNumber }, { allowLegacyUnknown: true });
      if (!String(clue.explanation || '').trim()) {
        warn('missing-explanation', 'Playable clue is missing an explanation', { index, date: g.date, secretItem: g.secretItem, clue: clueIndex + 1 });
      }
    });
  }
  if (g.format === 'v2' && !isStub) {
    const winnerSum = Number(g.goldWinners || 0) + Number(g.silverWinners || 0) + Number(g.bronzeWinners || 0);
    if (winnerSum !== Number(g.totalWinners || 0)) {
      error('v2-winner-total', 'v2 totalWinners does not equal medal winner sum', { index, date: g.date, secretItem: g.secretItem, winnerSum, totalWinners: g.totalWinners });
    }
    if (Number(g.silverWinners || 0) > 0 && Number(g.goldWinners || 0) === 0) {
      error('v2-medal-tier-order', 'v2 game cannot have silver winners without gold winners', { index, date: g.date, secretItem: g.secretItem });
    }
    if (Number(g.bronzeWinners || 0) > 0 && Number(g.silverWinners || 0) === 0) {
      error('v2-medal-tier-order', 'v2 game cannot have bronze winners when silver has no winners', { index, date: g.date, secretItem: g.secretItem });
    }
    const medalClues = [];
    for (const tier of ['gold', 'silver', 'bronze']) {
      const winners = Number(g[`${tier}Winners`] || 0);
      const clue = Number(g[`${tier}Clue`] || 0);
      if (winners > 0) {
        if (clue < 1 || clue > 5) {
          error('v2-medal-clue-range', 'v2 medal clue must be between 1 and 5 when that medal tier has winners', { index, date: g.date, secretItem: g.secretItem, tier, winners, clue });
        } else {
          medalClues.push(clue);
        }
      } else if (clue !== 0) {
        error('v2-empty-tier-clue', 'v2 medal clue must be omitted or 0 when that medal tier has no winners', { index, date: g.date, secretItem: g.secretItem, tier, clue });
      }
    }
    if (new Set(medalClues).size !== medalClues.length) {
      error('v2-medal-clues', 'v2 medal clue numbers are not distinct', { index, date: g.date, secretItem: g.secretItem, medalClues });
    }
    if (JSON.stringify(medalClues) !== JSON.stringify([...medalClues].sort((a, b) => a - b))) {
      error('v2-medal-clue-order', 'v2 medal clue numbers must be ordered earliest-to-latest: gold, silver, bronze', { index, date: g.date, secretItem: g.secretItem, medalClues });
    }
    if (g.winnerPayout !== '$7,500.00') {
      error('v2-winner-payout', 'v2 winnerPayout must remain the full round pot string "$7,500.00"', { index, date: g.date, secretItem: g.secretItem, winnerPayout: g.winnerPayout });
    }
    for (const field of ['goldPayout', 'silverPayout', 'bronzePayout']) {
      validatePayoutValue(g[field], field, { index, date: g.date, secretItem: g.secretItem });
    }
    const expectedPayouts = expectedV2Payouts(g);
    for (const field of ['goldPayout', 'silverPayout', 'bronzePayout']) {
      if (!moneyMatches(g[field], expectedPayouts[field])) {
        error('v2-payout-math', 'v2 payout does not match base pot plus no-winner redistribution math', { index, date: g.date, secretItem: g.secretItem, field, actual: g[field], expected: expectedPayouts[field] });
      }
    }
  } else if (!isStub) {
    if (g.format !== 'v1') {
      error('format-value', 'Playable game format must be "v1" or "v2"', { index, date: g.date, secretItem: g.secretItem, format: g.format });
    }
    const winningClue = validateCountValue(g.winningClue ?? g.goldClue, 'winningClue', { index, date: g.date, secretItem: g.secretItem });
    if (winningClue < 1 || winningClue > 5) {
      error('v1-winning-clue-range', 'v1 winningClue must be between 1 and 5', { index, date: g.date, secretItem: g.secretItem, winningClue });
    }
    const goldClue = validateCountValue(g.goldClue ?? winningClue, 'goldClue', { index, date: g.date, secretItem: g.secretItem });
    if (Number.isFinite(goldClue) && Number.isFinite(winningClue) && goldClue !== winningClue) {
      error('v1-gold-clue', 'v1 goldClue should match winningClue for compatibility', { index, date: g.date, secretItem: g.secretItem, winningClue, goldClue });
    }
    const totalWinners = validateCountValue(g.totalWinners, 'totalWinners', { index, date: g.date, secretItem: g.secretItem });
    const winnerCount = validateCountValue(g.winnerCount ?? g.totalWinners, 'winnerCount', { index, date: g.date, secretItem: g.secretItem });
    if (Number.isFinite(totalWinners) && Number.isFinite(winnerCount) && totalWinners !== winnerCount) {
      error('v1-winner-total', 'v1 winnerCount must equal totalWinners', { index, date: g.date, secretItem: g.secretItem, totalWinners, winnerCount });
    }
    if (Number.isFinite(winningClue) && Array.isArray(g.clues) && g.clues[winningClue - 1]) {
      const correctOnWinningClue = validateCountValue(g.clues[winningClue - 1].correct, 'correct', { index, date: g.date, secretItem: g.secretItem, clue: winningClue }, { allowLegacyUnknown: true });
      if (Number.isFinite(correctOnWinningClue) && Number.isFinite(totalWinners) && correctOnWinningClue !== totalWinners) {
        error('v1-winning-clue-count', 'v1 totalWinners must equal the correct count on winningClue', { index, date: g.date, secretItem: g.secretItem, winningClue, correctOnWinningClue, totalWinners });
      }
      for (let clueIndex = 0; clueIndex < winningClue - 1; clueIndex += 1) {
        const earlierCorrect = validateCountValue(g.clues[clueIndex].correct, 'correct', { index, date: g.date, secretItem: g.secretItem, clue: clueIndex + 1 }, { allowLegacyUnknown: true });
        if (Number.isFinite(earlierCorrect) && earlierCorrect !== 0) {
          error('v1-earliest-winning-clue', 'v1 winningClue must be the earliest clue with correct answers', { index, date: g.date, secretItem: g.secretItem, winningClue, earlierClue: clueIndex + 1, earlierCorrect });
        }
      }
    }
    validatePayoutValue(g.winnerPayout, 'winnerPayout', { index, date: g.date, secretItem: g.secretItem });
  }
  if (g.bonus && (!g.bonus.title || !g.bonus.desc)) {
    warn('bonus-shape', 'Bonus entry is missing title or desc', { index, date: g.date, secretItem: g.secretItem });
  }
}

for (const [date, rounds] of playableByDate.entries()) {
  if (archiveDateValue(date) >= archiveDateValue('Monday, May 11, 2026')) {
    const formats = rounds.map(g => g.format);
    if (formats.length === 2 && JSON.stringify(formats) !== JSON.stringify(['v2', 'v1'])) {
      error('hybrid-format-order', 'Episodes starting Monday, May 11, 2026 should import as Round 1 v2 and Round 2 v1 classic unless the broadcast says otherwise', { date, formats });
    }
  }
  const bonusRounds = rounds.filter(g => g.bonus).length;
  if (bonusRounds > 0 && bonusRounds < rounds.length) {
    warn('partial-day-bonus', 'Only some rounds on this date have bonus metadata', { date, bonusRounds, playableRounds: rounds.length });
  }
}

const transcriptDates = new Set();
for (const [index, t] of transcripts.entries()) {
  validateArchiveDate(t.date, { index, source: 'transcripts.json' });
  if (transcriptDates.has(t.date)) error('duplicate-transcript-date', 'Duplicate transcript date', { index, date: t.date });
  transcriptDates.add(t.date);
  const tags = (t.sections || []).map(section => section.tag);
  if (JSON.stringify(tags) !== JSON.stringify(expectedSections)) {
    error('transcript-section-order', 'Transcript does not use canonical six-section order', { index, date: t.date, tags });
  }
  for (const section of t.sections || []) {
    if (!Array.isArray(section.lines)) error('transcript-lines-shape', 'Transcript section lines is not an array', { date: t.date, section: section.tag });
    for (const line of section.lines || []) {
      if (!Object.hasOwn(line, 'speaker') || !Object.hasOwn(line, 'text')) {
        error('transcript-line-shape', 'Transcript line must contain speaker and text keys', { date: t.date, section: section.tag });
      }
      if (/[&](amp|lt|gt|quot|#\d+);/.test(line.text || '')) {
        error('escaped-html-entity', 'Transcript text contains escaped HTML entity that will display literally', { date: t.date, section: section.tag, text: line.text });
      }
    }
  }

  const relatedGames = playableByDate.get(t.date) || [];
  const expectedItems = relatedGames.map(g => g.secretItem);
  const actualItems = t.secretItems || [];
  if (JSON.stringify(expectedItems.map(loose)) !== JSON.stringify(actualItems.map(loose))) {
    error('transcript-secret-items', 'Transcript secretItems do not match games.json for date', { date: t.date, expectedItems, actualItems });
  }
  if ((t.rounds || []).length !== expectedItems.length) {
    error('transcript-round-count', 'Transcript rounds length does not match playable rounds for date', { date: t.date, expected: expectedItems.length, actual: (t.rounds || []).length });
  }
  (t.rounds || []).forEach((round, roundIndex) => {
    const game = relatedGames[roundIndex];
    if (!game) return;
    if (Number(round.round) !== roundIndex + 1) {
      error('transcript-round-number', 'Transcript round number is out of order', { date: t.date, roundIndex, actual: round.round });
    }
    if (loose(round.secretItem) !== loose(game.secretItem)) {
      error('transcript-round-secret-item', 'Transcript round secretItem does not match games.json', { date: t.date, round: roundIndex + 1, expected: game.secretItem, actual: round.secretItem });
    }
  });

  const resultSections = (t.sections || []).filter(section => /Results/i.test(section.tag));
  relatedGames.forEach((game, roundIndex) => {
    const section = resultSections[roundIndex];
    if (!section) return;
    const resultText = (section.lines || []).map(line => line.text || '').join('\n');
    for (let clueIndex = 0; clueIndex < 5; clueIndex += 1) {
      const clueText = game.clues?.[clueIndex]?.text;
      if (clueText && !loose(resultText).includes(loose(clueText))) {
        error('result-missing-clue', 'Result section is missing expected clue text', { date: t.date, round: roundIndex + 1, clue: clueIndex + 1, secretItem: game.secretItem, clueText });
      }
    }
  });
}

for (const date of allDates) {
  if (!transcriptDates.has(date)) error('missing-transcript', 'Game date has no transcript entry', { date });
}
for (const date of transcriptDates) {
  if (!allDates.has(date)) warn('orphan-transcript', 'Transcript date has no matching game date', { date });
}

const summary = {
  ok: !issues.some(issue => issue.level === 'error'),
  errors: issues.filter(issue => issue.level === 'error').length,
  warnings: issues.filter(issue => issue.level === 'warn').length,
  fixes,
  counts: {
    games: games.length,
    meta: meta.length,
    transcripts: transcripts.length,
    gameDates: allDates.size,
    inlineScripts: inlineScriptCount
  },
  issues
};

if (asJson) {
  console.log(JSON.stringify(summary, null, 2));
} else {
  console.log(`Data audit: ${summary.ok ? 'PASS' : 'FAIL'}`);
  console.log(`Games: ${games.length} | Meta: ${meta.length} | Transcripts: ${transcripts.length} | Dates: ${allDates.size} | Inline scripts: ${inlineScriptCount}`);
  console.log(`Errors: ${summary.errors} | Warnings: ${summary.warnings}`);
  for (const fix of fixes) {
    console.log(`[FIXED] ${fix.code}: ${fix.path}`);
  }
  for (const issue of issues.slice(0, 60)) {
    console.log(`[${issue.level.toUpperCase()}] ${issue.code}: ${issue.message}${issue.date ? ` (${issue.date})` : ''}`);
  }
  if (issues.length > 60) console.log(`...and ${issues.length - 60} more issues`);
}

if (!summary.ok) process.exitCode = 1;
