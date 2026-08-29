# Gemini gap-fill prompts

One prompt per episode date that still has a hole in the archive. Paste a block
into Gemini together with that date's YouTube video.

These are **not** the full-episode import prompt (`docs/DAILY_IMPORT_PROMPT.md` /
the "Copy Gemini Prompt" button). Every date below is already imported — these
ask only for the specific fields that are missing, so Gemini has far less room
to invent, and the reply is small enough to check by eye.

**When a reply comes back, hand it to Claude as-is.** Do not merge it yourself:
counts get re-checked against `floorCents()` before anything is written, and a
guess count that contradicts a stored payout has to be caught, not stored.

**If Gemini answers `null` for something, that is a good answer** — it means the
figure was never on screen. Send the `null` through; the archive already has a
convention for unknown counts (`"N/A"`) and a fabricated number is much worse
than an honest gap.

## What is outstanding

| Gap | Dates | Notes |
| --- | --- | --- |
| Missing `guesses` counts | 16 | Dec 9, 2025 – Jan 15, 2026. Early episodes; the results card often showed correct-only. |
| Missing `correct` counts | 7 | Same window, same cause. |
| Missing winner names | 20 | Scattered Jan–Aug 2026. Usernames the host reads out. |
| Missing clue-5 explanation | 3 | Aug 14, 24, 25, 2026 — may genuinely not exist; see below. |

Total: **38 dates** still need something. Nothing is left to verify by eye.

**Resolved so far**

- *Apr 8, 2026 (SKUNK clue 5) — real figures 2,202 correct of 2,504 guesses; the
  stored `254` was `2,504` with a digit dropped.*
- *Feb 17, 2026 (PARADE / MOON) — the full transcript confirmed that every
  `correct` value was already right and that PARADE's entire guesses column had
  been overwritten with MOON's. Real PARADE guesses are 50,982 / 13,447 / 6,361 /
  6,821 for clues 2–5. Two figures stay unknown and are listed below: PARADE
  clue 1 (the host says it, but the source transcript garbles it to "6,63") and
  MOON clue 5 (never stated aloud).*
- *Aug 20, 2026 (MIRROR / KEANU REEVES) — **false alarm, nothing was wrong.** The
  transcript confirms all twenty figures exactly as stored, and all six payouts
  reproduce. MIRROR clue 5's 4,883 / 5,141 really are its numbers; that they also
  appear as BUTTERFLY's guess counts on Aug 12 is coincidence, and note they sit
  in different roles there (both are guess counts on Aug 12, but correct-and-guesses
  on Aug 20), which is what a real copy would not do.*

---

## § NotebookLM — nine small prompts

**⚠️ A single combined sweep does not work.** It timed out, and when it did
answer it returned an entirely fabricated table: every date was paired with the
wrong answer, and three answers (SLOTH, ANCHORMAN, CAST) do not exist in the
archive at all. Not one row was usable. Run these nine instead, one at a time.

Each one names the expected answer for every date and tells the model to report
`MISMATCH` rather than substitute an episode — that guard is what the failed
sweep lacked. **Check the answer names in the reply against the ones in the
prompt before sending anything on.**


### A1 of 5 — counts

```
Best Guess Live. For each episode below, use the part after the answer is revealed where the host reviews each clue. Output rows only, nothing else.

Format, one row per round:
DATE | ANSWER | 1:guesses/correct | 2:g/c | 3:g/c | 4:g/c | 5:g/c

Episodes:
- Dec 9, 2025 — CHATGPT and MOUNT RUSHMORE
- Dec 10, 2025 — JAMES BOND and S'MORES
- Dec 11, 2025 — M&MS and TITANIC
- Dec 12, 2025 — GOODYEAR BLIMP and BIRTHDAY CAKE

I have given you the correct answer for each episode. Verify it before answering: if the episode you find for a date has a DIFFERENT answer, write MISMATCH and the answer you actually found, and move on. Never substitute a different episode, and never answer for a date that is not listed.

Copy numbers exactly as the host says them, digits only. Write null if he never says one. Never estimate a number or work it back from a prize amount.
```

### A2 of 5 — counts

```
Best Guess Live. For each episode below, use the part after the answer is revealed where the host reviews each clue. Output rows only, nothing else.

Format, one row per round:
DATE | ANSWER | 1:guesses/correct | 2:g/c | 3:g/c | 4:g/c | 5:g/c

Episodes:
- Dec 15, 2025 — PARIS HILTON and MONOPOLY
- Dec 16, 2025 — THE GRINCH and BOWLING
- Dec 17, 2025 — RUDOLPH THE RED-NOSED REINDEER and OREO
- Dec 18, 2025 — KING KONG and FRENCH FRIES

I have given you the correct answer for each episode. Verify it before answering: if the episode you find for a date has a DIFFERENT answer, write MISMATCH and the answer you actually found, and move on. Never substitute a different episode, and never answer for a date that is not listed.

Copy numbers exactly as the host says them, digits only. Write null if he never says one. Never estimate a number or work it back from a prize amount.
```

### A3 of 5 — counts

```
Best Guess Live. For each episode below, use the part after the answer is revealed where the host reviews each clue. Output rows only, nothing else.

Format, one row per round:
DATE | ANSWER | 1:guesses/correct | 2:g/c | 3:g/c | 4:g/c | 5:g/c

Episodes:
- Dec 22, 2025 — PINOCCHIO and WILL FERRELL
- Dec 25, 2025 — GARBAGE TRUCK and CRUTCHES
- Dec 26, 2025 — BAGGAGE CLAIM and ICE CUBE TRAY
- Dec 29, 2025 — WONDER WOMAN and CAVITY

I have given you the correct answer for each episode. Verify it before answering: if the episode you find for a date has a DIFFERENT answer, write MISMATCH and the answer you actually found, and move on. Never substitute a different episode, and never answer for a date that is not listed.

Copy numbers exactly as the host says them, digits only. Write null if he never says one. Never estimate a number or work it back from a prize amount.
```

### A4 of 5 — counts

```
Best Guess Live. For each episode below, use the part after the answer is revealed where the host reviews each clue. Output rows only, nothing else.

Format, one row per round:
DATE | ANSWER | 1:guesses/correct | 2:g/c | 3:g/c | 4:g/c | 5:g/c

Episodes:
- Dec 30, 2025 — MCDONALD'S and SANDCASTLE
- Jan 1, 2026 — KENTUCKY DERBY and JOKE
- Jan 13, 2026 — ENGAGEMENT RING and PEPPERONI
- Jan 15, 2026 — COSTCO and HARMONICA

I have given you the correct answer for each episode. Verify it before answering: if the episode you find for a date has a DIFFERENT answer, write MISMATCH and the answer you actually found, and move on. Never substitute a different episode, and never answer for a date that is not listed.

Copy numbers exactly as the host says them, digits only. Write null if he never says one. Never estimate a number or work it back from a prize amount.
```

### A5 of 5 — counts

```
Best Guess Live. For each episode below, use the part after the answer is revealed where the host reviews each clue. Output rows only, nothing else.

Format, one row per round:
DATE | ANSWER | 1:guesses/correct | 2:g/c | 3:g/c | 4:g/c | 5:g/c

Episodes:
- Feb 17, 2026 — PARADE and MOON

I have given you the correct answer for each episode. Verify it before answering: if the episode you find for a date has a DIFFERENT answer, write MISMATCH and the answer you actually found, and move on. Never substitute a different episode, and never answer for a date that is not listed.

Copy numbers exactly as the host says them, digits only. Write null if he never says one. Never estimate a number or work it back from a prize amount.
```

### B1 of 3 — winner names

```
Best Guess Live. For each round below, find where the host reads out the winners' usernames after announcing the payout. Output rows only, nothing else.

Format, one row per round:
DATE | ANSWER | WINNERS: name, name, name

Rounds:
- Jan 20, 2026 — AVOCADO
- Feb 6, 2026 — SCARECROW
- Feb 12, 2026 — PENCIL SHARPENER
- Feb 26, 2026 — TABLE LEAF
- Mar 25, 2026 — QUICKSAND
- Mar 31, 2026 — SNOOP DOGG

I have given you the correct answer for each episode. Verify it before answering: if the episode you find for a date has a DIFFERENT answer, write MISMATCH and the answer you actually found, and move on. Never substitute a different episode, and never answer for a date that is not listed.

Spell usernames exactly as said. Write null if the host names no winners for that round. Do not invent names.
```

### B2 of 3 — winner names

```
Best Guess Live. For each round below, find where the host reads out the winners' usernames after announcing the payout. Output rows only, nothing else.

Format, one row per round:
DATE | ANSWER | WINNERS: name, name, name

Rounds:
- Apr 1, 2026 — SUNGLASSES
- Apr 20, 2026 — MUHAMMAD ALI
- May 1, 2026 — ZOOM
- May 1, 2026 — JUMPING JACKS
- May 8, 2026 — LEBRON JAMES
- Jun 5, 2026 — SUNBURN
- Jun 5, 2026 — TOM HANKS
- Jun 9, 2026 — TACO BELL

I have given you the correct answer for each episode. Verify it before answering: if the episode you find for a date has a DIFFERENT answer, write MISMATCH and the answer you actually found, and move on. Never substitute a different episode, and never answer for a date that is not listed.

Spell usernames exactly as said. Write null if the host names no winners for that round. Do not invent names.
```

### B3 of 3 — winner names

```
Best Guess Live. For each round below, find where the host reads out the winners' usernames after announcing the payout. Output rows only, nothing else.

Format, one row per round:
DATE | ANSWER | WINNERS: name, name, name

Rounds:
- Jun 15, 2026 — SEATBELT
- Jun 24, 2026 — NIGHTMARE
- Jun 26, 2026 — POPCORN
- Jun 29, 2026 — MARIO
- Jul 31, 2026 — PITBULL
- Aug 26, 2026 — MILKSHAKE

I have given you the correct answer for each episode. Verify it before answering: if the episode you find for a date has a DIFFERENT answer, write MISMATCH and the answer you actually found, and move on. Never substitute a different episode, and never answer for a date that is not listed.

Spell usernames exactly as said. Write null if the host names no winners for that round. Do not invent names.
```

### C of 1 — clue-5 explanations

```
Best Guess Live. For each round below, find where the host reviews clue 5 after the answer is revealed, and tell me how he explains what clue 5 meant. Output rows only, nothing else.

Format:
DATE | ANSWER | CLUE 5 MEANING: ...

Rounds:
- Aug 14, 2026 — BIG BEN
- Aug 24, 2026 — BATMAN
- Aug 25, 2026 — MULLET

I have given you the correct answer for each episode. Verify it before answering: if the episode you find for a date has a DIFFERENT answer, write MISMATCH and the answer you actually found, and move on. Never substitute a different episode, and never answer for a date that is not listed.

Quote the host's own words. If he reads clue 5 out but never explains it, write null — do not explain the wordplay yourself.
```

---

## § Not in NotebookLM

**Dec 16, 2025 (THE GRINCH / BOWLING)** was silently absent from an otherwise
clean reply covering Dec 15–18 — the notebook appears not to hold that
transcript. Worth adding before re-running the Dec 15–18 batch.

---

## § Disputed values — not imported, need a second look

Returned by a NotebookLM run whose answer names all checked out, but each of
these is shape-anomalous and single-sourced, so none was stored. Re-ask or watch
before acting.

| Date | Round | Clue | Stored | Reply said | Why it was not taken |
| --- | --- | --- | --- | --- | --- |
| Dec 12, 2025 | GOODYEAR BLIMP | 1 guesses | 2,542 | 25,542 | Other clues are 2,000 and 3,000; 25,542 is ten times the round's shape. |
| Dec 11, 2025 | M&MS | 2 guesses | 2,094 | 294 | Other clues are 3,249 and 2,832; 294 is an order out. |
| Dec 9, 2025 | CHATGPT | 5 guesses | *(unknown)* | 719 | Equals its own `correct` exactly — a 100% hit rate, the same artifact that was proven wrong on Feb 17's MOON clue 5. |
| Dec 10, 2025 | S'MORES | 5 guesses | *(unknown)* | 11,996 | Other clues run 1,335–1,880. Guess counts fall across a round in every verified example; a 6× spike on clue 5 does not fit. |
| Dec 15, 2025 | PARIS HILTON | 2 guesses | 11,286 | 2,200 | Round has 237 on clue 1 and 4,000 on clue 5; neither figure sits comfortably between them and both are single-sourced. |

---

## § Verification — all resolved

Nothing left to check by eye. For the record:

- **Apr 8, 2026 — SKUNK clue 5.** Real figures 2,202 correct of 2,504 guesses; the
  stored `254` was `2,504` with a digit dropped.
- **Feb 17, 2026 — PARADE / MOON.** PARADE's whole guesses column had been
  overwritten with MOON's. Every `correct` value was already right.
- **Aug 20, 2026 — MIRROR / KEANU REEVES.** False alarm; all twenty figures and
  all six payouts were already correct.
- **Aug 13, 2026 — YO-YO.** The on-screen answer card is hyphenated, so
  `secretItem` moved from `YO YO` to `YO-YO`. This also matches clue 2's stored
  explanation, which turns on "the word yo-yo has a hyphen in the middle of it".

---

## § A note on the three missing explanations

Aug 14 (BIG BEN), Aug 24 (BATMAN) and Aug 25 (MULLET) are each missing the
explanation for clue 5 — always the rhyming giveaway clue. The pattern suggests
the host simply does not explain the final clue when it gives the answer away,
in which case **`null` is the correct answer and these three can be closed**.

---

## § Per-date prompts

### Tuesday, December 9, 2025 — CHATGPT / MOUNT RUSHMORE

```
Best Guess Live, Tuesday, December 9, 2025. Round 1 answer was CHATGPT. Round 2 answer was MOUNT RUSHMORE.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (CHATGPT): `guesses` (total submissions) for clues 3, 4, 5
- Round 2 (MOUNT RUSHMORE): `guesses` (total submissions) for clues 4, 5

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Tuesday, December 9, 2025", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Wednesday, December 10, 2025 — JAMES BOND / S'MORES

```
Best Guess Live, Wednesday, December 10, 2025. Round 1 answer was JAMES BOND. Round 2 answer was S'MORES.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (JAMES BOND): `guesses` (total submissions) for clues 2, 5
- Round 2 (S'MORES): `guesses` (total submissions) for clue 5

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Wednesday, December 10, 2025", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Thursday, December 11, 2025 — M&MS / TITANIC

```
Best Guess Live, Thursday, December 11, 2025. Round 1 answer was M&MS. Round 2 answer was TITANIC.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (M&MS): `guesses` (total submissions) for clues 3, 4
- Round 2 (TITANIC): `guesses` (total submissions) for clue 4

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Thursday, December 11, 2025", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Friday, December 12, 2025 — GOODYEAR BLIMP / BIRTHDAY CAKE

```
Best Guess Live, Friday, December 12, 2025. Round 1 answer was GOODYEAR BLIMP. Round 2 answer was BIRTHDAY CAKE.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (GOODYEAR BLIMP): `guesses` (total submissions) for clues 4, 5
- Round 2 (BIRTHDAY CAKE): `guesses` (total submissions) for clues 1, 3, 4, 5

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Friday, December 12, 2025", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Monday, December 15, 2025 — PARIS HILTON / MONOPOLY

```
Best Guess Live, Monday, December 15, 2025. Round 1 answer was PARIS HILTON. Round 2 answer was MONOPOLY.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (PARIS HILTON): `guesses` (total submissions) for clues 3, 4, 5
- Round 2 (MONOPOLY): `guesses` (total submissions) for clues 3, 5

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Monday, December 15, 2025", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Tuesday, December 16, 2025 — THE GRINCH / BOWLING

```
Best Guess Live, Tuesday, December 16, 2025. Round 1 answer was THE GRINCH. Round 2 answer was BOWLING.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (THE GRINCH): `guesses` (total submissions) for clues 1, 2, 3, 4, 5
- Round 2 (BOWLING): `correct` count for clue 5; `guesses` (total submissions) for clues 2, 4, 5

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Tuesday, December 16, 2025", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Wednesday, December 17, 2025 — RUDOLPH THE RED-NOSED REINDEER / OREO

```
Best Guess Live, Wednesday, December 17, 2025. Round 1 answer was RUDOLPH THE RED-NOSED REINDEER. Round 2 answer was OREO.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (RUDOLPH THE RED-NOSED REINDEER): `correct` count for clues 4, 5; `guesses` (total submissions) for clues 2, 4, 5
- Round 2 (OREO): `guesses` (total submissions) for clues 2, 3, 4, 5

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Wednesday, December 17, 2025", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Thursday, December 18, 2025 — KING KONG / FRENCH FRIES

```
Best Guess Live, Thursday, December 18, 2025. Round 1 answer was KING KONG. Round 2 answer was FRENCH FRIES.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (KING KONG): `guesses` (total submissions) for clues 2, 4, 5
- Round 2 (FRENCH FRIES): `guesses` (total submissions) for clue 5

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Thursday, December 18, 2025", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Monday, December 22, 2025 — PINOCCHIO / WILL FERRELL

```
Best Guess Live, Monday, December 22, 2025. Round 1 answer was PINOCCHIO. Round 2 answer was WILL FERRELL.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (PINOCCHIO): `guesses` (total submissions) for clue 4
- Round 2 (WILL FERRELL): `guesses` (total submissions) for clues 2, 3, 4

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Monday, December 22, 2025", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Thursday, December 25, 2025 — GARBAGE TRUCK / CRUTCHES

```
Best Guess Live, Thursday, December 25, 2025. Round 1 answer was GARBAGE TRUCK. Round 2 answer was CRUTCHES.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (CRUTCHES): `correct` count for clue 3; `guesses` (total submissions) for clue 3

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Thursday, December 25, 2025", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Friday, December 26, 2025 — BAGGAGE CLAIM / ICE CUBE TRAY

```
Best Guess Live, Friday, December 26, 2025. Round 1 answer was BAGGAGE CLAIM. Round 2 answer was ICE CUBE TRAY.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (ICE CUBE TRAY): `guesses` (total submissions) for clue 5

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Friday, December 26, 2025", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Monday, December 29, 2025 — WONDER WOMAN / CAVITY

```
Best Guess Live, Monday, December 29, 2025. Round 1 answer was WONDER WOMAN. Round 2 answer was CAVITY.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (CAVITY): `correct` count for clue 5; `guesses` (total submissions) for clues 4, 5

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Monday, December 29, 2025", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Tuesday, December 30, 2025 — MCDONALD'S / SANDCASTLE

```
Best Guess Live, Tuesday, December 30, 2025. Round 1 answer was MCDONALD'S. Round 2 answer was SANDCASTLE.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (SANDCASTLE): `correct` count for clue 5; `guesses` (total submissions) for clue 5

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Tuesday, December 30, 2025", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Thursday, January 1, 2026 — KENTUCKY DERBY / JOKE

```
Best Guess Live, Thursday, January 1, 2026. Round 1 answer was KENTUCKY DERBY. Round 2 answer was JOKE.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (KENTUCKY DERBY): `correct` count for clue 5; `guesses` (total submissions) for clue 5

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Thursday, January 1, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Tuesday, January 13, 2026 — ENGAGEMENT RING / PEPPERONI

```
Best Guess Live, Tuesday, January 13, 2026. Round 1 answer was ENGAGEMENT RING. Round 2 answer was PEPPERONI.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (ENGAGEMENT RING): `guesses` (total submissions) for clues 4, 5
- Round 2 (PEPPERONI): `guesses` (total submissions) for clue 5

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Tuesday, January 13, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Thursday, January 15, 2026 — COSTCO / HARMONICA

```
Best Guess Live, Thursday, January 15, 2026. Round 1 answer was COSTCO. Round 2 answer was HARMONICA.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (COSTCO): `guesses` (total submissions) for clue 4
- Round 2 (HARMONICA): `guesses` (total submissions) for clue 5

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Thursday, January 15, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Tuesday, January 20, 2026 — SCUBA DIVING / AVOCADO

```
Best Guess Live, Tuesday, January 20, 2026. Round 1 answer was SCUBA DIVING. Round 2 answer was AVOCADO.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (AVOCADO): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Tuesday, January 20, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Friday, February 6, 2026 — CUTTING BOARD / SCARECROW

```
Best Guess Live, Friday, February 6, 2026. Round 1 answer was CUTTING BOARD. Round 2 answer was SCARECROW.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (SCARECROW): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Friday, February 6, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Thursday, February 12, 2026 — PICKUP LINE / PENCIL SHARPENER

```
Best Guess Live, Thursday, February 12, 2026. Round 1 answer was PICKUP LINE. Round 2 answer was PENCIL SHARPENER.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (PENCIL SHARPENER): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Thursday, February 12, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Tuesday, February 17, 2026 — PARADE / MOON

```
Best Guess Live, Tuesday, February 17, 2026. Round 1 answer was PARADE. Round 2 answer was MOON.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (PARADE): `guesses` (total submissions) for clue 1
- Round 2 (MOON): `guesses` (total submissions) for clue 5

**Rules — read before answering:**
- The on-screen results card is the only source of truth for numbers. If a figure is never shown on screen, say `null` for it rather than guessing — do not infer it from the payout, from other clues, or from what sounds plausible.
- If the host says a number aloud but it is never shown on screen, give the number and set `"heardOnly": true` for that round.
- Do not round. Give counts exactly as displayed, digits only (no commas needed).
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Tuesday, February 17, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Thursday, February 26, 2026 — SNEEZE / TABLE LEAF

```
Best Guess Live, Thursday, February 26, 2026. Round 1 answer was SNEEZE. Round 2 answer was TABLE LEAF.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (TABLE LEAF): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Thursday, February 26, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Wednesday, March 25, 2026 — QUICKSAND / SURF AND TURF

```
Best Guess Live, Wednesday, March 25, 2026. Round 1 answer was QUICKSAND. Round 2 answer was SURF AND TURF.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (QUICKSAND): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Wednesday, March 25, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Tuesday, March 31, 2026 — HIGH HEELS / SNOOP DOGG

```
Best Guess Live, Tuesday, March 31, 2026. Round 1 answer was HIGH HEELS. Round 2 answer was SNOOP DOGG.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (SNOOP DOGG): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Tuesday, March 31, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Wednesday, April 1, 2026 — SUNGLASSES / EMOJI

```
Best Guess Live, Wednesday, April 1, 2026. Round 1 answer was SUNGLASSES. Round 2 answer was EMOJI.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (SUNGLASSES): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Wednesday, April 1, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Monday, April 20, 2026 — RAINBOW / MUHAMMAD ALI

```
Best Guess Live, Monday, April 20, 2026. Round 1 answer was RAINBOW. Round 2 answer was MUHAMMAD ALI.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (MUHAMMAD ALI): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Monday, April 20, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Friday, May 1, 2026 — ZOOM / JUMPING JACKS

```
Best Guess Live, Friday, May 1, 2026. Round 1 answer was ZOOM. Round 2 answer was JUMPING JACKS.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (ZOOM): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)
- Round 2 (JUMPING JACKS): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Friday, May 1, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Friday, May 8, 2026 — LEBRON JAMES / YODELING

```
Best Guess Live, Friday, May 8, 2026. Round 1 answer was LEBRON JAMES. Round 2 answer was YODELING.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (LEBRON JAMES): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Friday, May 8, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Friday, June 5, 2026 — SUNBURN / TOM HANKS

```
Best Guess Live, Friday, June 5, 2026. Round 1 answer was SUNBURN. Round 2 answer was TOM HANKS.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (SUNBURN): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)
- Round 2 (TOM HANKS): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Friday, June 5, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Tuesday, June 9, 2026 — TACO BELL / TOM CRUISE

```
Best Guess Live, Tuesday, June 9, 2026. Round 1 answer was TACO BELL. Round 2 answer was TOM CRUISE.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (TACO BELL): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Tuesday, June 9, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Monday, June 15, 2026 — CANDLE / SEATBELT

```
Best Guess Live, Monday, June 15, 2026. Round 1 answer was CANDLE. Round 2 answer was SEATBELT.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (SEATBELT): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Monday, June 15, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Wednesday, June 24, 2026 — NIGHTMARE / BUTT DIAL

```
Best Guess Live, Wednesday, June 24, 2026. Round 1 answer was NIGHTMARE. Round 2 answer was BUTT DIAL.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (NIGHTMARE): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Wednesday, June 24, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Friday, June 26, 2026 — SURFBOARD / POPCORN

```
Best Guess Live, Friday, June 26, 2026. Round 1 answer was SURFBOARD. Round 2 answer was POPCORN.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (POPCORN): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Friday, June 26, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Monday, June 29, 2026 — FLAMINGO / MARIO

```
Best Guess Live, Monday, June 29, 2026. Round 1 answer was FLAMINGO. Round 2 answer was MARIO.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (MARIO): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Monday, June 29, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Friday, July 31, 2026 — PINEAPPLE / PITBULL

```
Best Guess Live, Friday, July 31, 2026. Round 1 answer was PINEAPPLE. Round 2 answer was PITBULL.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (PITBULL): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Friday, July 31, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Friday, August 14, 2026 — MATT DAMON / BIG BEN

```
Best Guess Live, Friday, August 14, 2026. Round 1 answer was MATT DAMON. Round 2 answer was BIG BEN.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (BIG BEN): the host's spoken explanation of clue 5 — one sentence, what the clue meant. If the host never explains it, return `null`.

**Rules — read before answering:**
- Quote the host's actual words for an explanation. If the host never explains that clue, return `null` — do not write your own explanation of the wordplay.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Friday, August 14, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Monday, August 24, 2026 — PENGUIN / BATMAN

```
Best Guess Live, Monday, August 24, 2026. Round 1 answer was PENGUIN. Round 2 answer was BATMAN.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (BATMAN): the host's spoken explanation of clue 5 — one sentence, what the clue meant. If the host never explains it, return `null`.

**Rules — read before answering:**
- Quote the host's actual words for an explanation. If the host never explains that clue, return `null` — do not write your own explanation of the wordplay.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Monday, August 24, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Tuesday, August 25, 2026 — MULLET / K-POP

```
Best Guess Live, Tuesday, August 25, 2026. Round 1 answer was MULLET. Round 2 answer was K-POP.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 1 (MULLET): the host's spoken explanation of clue 5 — one sentence, what the clue meant. If the host never explains it, return `null`.

**Rules — read before answering:**
- Quote the host's actual words for an explanation. If the host never explains that clue, return `null` — do not write your own explanation of the wordplay.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Tuesday, August 25, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```

### Wednesday, August 26, 2026 — ZIPPER / MILKSHAKE

```
Best Guess Live, Wednesday, August 26, 2026. Round 1 answer was ZIPPER. Round 2 answer was MILKSHAKE.
This episode is already archived — I do not need a transcript or a re-import. I need only the specific values below, which are missing from my records.

**What I need:**
- Round 2 (MILKSHAKE): the winner usernames the host reads out (comma-separated, exactly as spelled on screen)

**Rules — read before answering:**
- Take usernames from the on-screen winners list, not from the host saying them aloud — hosts mispronounce them. If they are never shown on screen, transcribe what the host says and set `"heardOnly": true` for that round.
- If no winner names are shown or read at all, say `null` rather than guessing.
- Do not re-transcribe the episode and do not return any field I did not ask for.

**Output:** one JSON object and nothing else — no markdown fences, no commentary — shaped as {"date": "Wednesday, August 26, 2026", "round1": {...}, "round2": {...}}. Use only the keys listed under "What I need" for each round, and omit a round entirely if I did not ask for anything from it.
```
