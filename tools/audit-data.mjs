import fs from 'node:fs';
import vm from 'node:vm';

const asJson = process.argv.includes('--json');
const expectedSections = ['Intro', 'Round 1', 'Round 1 Results', 'Round 2', 'Round 2 Results', 'Outro'];
const readJson = path => JSON.parse(fs.readFileSync(path, 'utf8'));
const loose = value => String(value || '')
  .normalize('NFKD')
  .replace(/[’']/g, '')
  .replace(/&/g, 'AND')
  .replace(/[^A-Z0-9]+/gi, '')
  .toUpperCase();

const games = readJson('data/games.json');
const meta = readJson('data/games-meta.json');
const transcripts = readJson('data/transcripts.json');
const issues = [];
const warn = (code, message, context = {}) => issues.push({ level: 'warn', code, message, ...context });
const error = (code, message, context = {}) => issues.push({ level: 'error', code, message, ...context });

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
  if (g.note) entry.note = g.note;
  return entry;
});

if (JSON.stringify(regeneratedMeta) !== JSON.stringify(meta)) {
  error('meta-mismatch', 'data/games-meta.json does not regenerate exactly from data/games.json');
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
  const isStub = !!g.note || (!g.secretItem && (!g.clues || !g.clues.length));
  if (!playableByDate.has(g.date)) playableByDate.set(g.date, []);
  if (!isStub) playableByDate.get(g.date).push(g);

  if (!isStub && (!Array.isArray(g.clues) || g.clues.length !== 5)) {
    error('clue-count', 'Playable game does not have exactly five clues', { index, date: g.date, secretItem: g.secretItem });
  }
  if (g.format === 'v2' && !isStub) {
    const winnerSum = Number(g.goldWinners || 0) + Number(g.silverWinners || 0) + Number(g.bronzeWinners || 0);
    if (winnerSum !== Number(g.totalWinners || 0)) {
      error('v2-winner-total', 'v2 totalWinners does not equal medal winner sum', { index, date: g.date, secretItem: g.secretItem, winnerSum, totalWinners: g.totalWinners });
    }
    const medalClues = [g.goldClue, g.silverClue, g.bronzeClue].map(Number).filter(Boolean);
    if (new Set(medalClues).size !== medalClues.length) {
      error('v2-medal-clues', 'v2 medal clue numbers are not distinct', { index, date: g.date, secretItem: g.secretItem, medalClues });
    }
  }
  if (g.bonus && (!g.bonus.title || !g.bonus.desc)) {
    warn('bonus-shape', 'Bonus entry is missing title or desc', { index, date: g.date, secretItem: g.secretItem });
  }
}

for (const [date, rounds] of playableByDate.entries()) {
  const bonusRounds = rounds.filter(g => g.bonus).length;
  if (bonusRounds > 0 && bonusRounds < rounds.length) {
    warn('partial-day-bonus', 'Only some rounds on this date have bonus metadata', { date, bonusRounds, playableRounds: rounds.length });
  }
}

const transcriptDates = new Set();
for (const [index, t] of transcripts.entries()) {
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
  for (const issue of issues.slice(0, 60)) {
    console.log(`[${issue.level.toUpperCase()}] ${issue.code}: ${issue.message}${issue.date ? ` (${issue.date})` : ''}`);
  }
  if (issues.length > 60) console.log(`...and ${issues.length - 60} more issues`);
}

if (!summary.ok) process.exitCode = 1;
