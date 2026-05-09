# Plaud Audio Prompt

Use this with Plaud or another audio-only transcription tool. It should only use what can be heard in the episode audio, and it should mark anything uncertain instead of inventing it.

```text
You are transcribing a Best Guess Live episode for structured archival import. This is a Netflix game show: two rounds, each with five clues revealed one at a time, players guess a secret item, then a crystal ball opens to reveal the answer and prize payouts.

Output in this exact structure:

DATE: [Weekday, Month D, YYYY - use today's date unless stated otherwise]
HOST: [Howie Mandel or Hunter March and/or guest hosts who identify themselves by name]
ROUND 1 ANSWER: [secret item revealed when crystal ball opens]
ROUND 2 ANSWER: [secret item revealed when crystal ball opens]
ROUND 1 FORMAT: [v2 tiered unless the episode says otherwise]
ROUND 2 FORMAT: [Before Monday, May 11, 2026 usually v2 tiered. Starting Monday, May 11, 2026 use v1 classic unless the episode says otherwise.]

---

[INTRO]
Host Name: [verbatim sentence]
Host Name: [verbatim sentence]

[ROUND 1]
Host Name: [verbatim sentence]

[ROUND 1 RESULTS]
Host Name: [verbatim sentence]
CLUE COUNTS: Clue 5: [N] correct / [N] total guesses | Clue 4: [N] correct / [N] total guesses | Clue 3: [N] correct / [N] total guesses | Clue 2: [N] correct / [N] total guesses | Clue 1: [N] correct / [N] total guesses
WINNER DATA: Gold [N] winner(s) at $[X] each | Silver [N] winner(s) at $[X] each | Bronze [N] winner(s) at $[X] each
WINNER NAMES: [all names read aloud]

[ROUND 2]
Host Name: [verbatim sentence]

[ROUND 2 RESULTS]
Host Name: [verbatim sentence]
CLUE COUNTS: Clue 5: [N] correct / [N] total guesses | Clue 4: [N] correct / [N] total guesses | Clue 3: [N] correct / [N] total guesses | Clue 2: [N] correct / [N] total guesses | Clue 1: [N] correct / [N] total guesses
WINNER DATA V2: Gold [N] winner(s) at $[X] each | Silver [N] winner(s) at $[X] each | Bronze [N] winner(s) at $[X] each
WINNER DATA V1 CLASSIC: Winning Clue [1-5] | Winner Count [N] | Winner Payout $[X] each | Total Pot $7,500
WINNER NAMES: [all names read aloud]

[OUTRO]
Host Name: [verbatim sentence]
BONUS PRIZE: [exact description and price if a weekly bonus prize is announced, otherwise omit]

---

Rules:
- Every spoken sentence is its own labeled line. One sentence per line. Never merge or paraphrase.
- Include every joke, tangent, time countdown, and transition - nothing skipped.
- When the host calls out a player's wrong guess, capture it: Host Name: "[Username] said [guess]."
- In Results sections, capture the host's explanation for each clue exactly as spoken before the CLUE COUNTS line.
- Capture payout amounts and winner names exactly as announced. If the host says "each" or "a piece," note it.
- Use the full host name on every line: "Howie Mandel" or "Hunter March."
- Infer clue spelling as best as possible from audio only. If spelling or punctuation is uncertain, add [?] immediately after the uncertain word or phrase.
- Do not include any information that is not spoken aloud. If popular wrong guesses, clue wording, counts, or payouts are not spoken clearly, write [not spoken] or [unclear] rather than guessing.
- Starting Monday, May 11, 2026, Round 2 is classic mode unless the episode says otherwise: only the earliest clue with any correct answers wins, and those winners split the full $7,500 pot. In that case fill WINNER DATA V1 CLASSIC and leave WINNER DATA V2 as "not applicable."
- For v2 tiered rounds, fill WINNER DATA V2 and leave WINNER DATA V1 CLASSIC as "not applicable."
- If a silver or bronze v2 tier has no winners, write 0 winners at $0 and keep all five clue counts.
```
