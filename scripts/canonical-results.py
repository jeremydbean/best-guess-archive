#!/usr/bin/env python3
"""Reformat Apr 29/30 Results sections to canonical structure (verbatim banter
preserved, but with structured null-speaker per-clue recap + medal summary)."""
import json

APR30_R1_RESULTS = [
    {"speaker": "Howie Mandel", "text": "Open that ball right now! THE WAVE! The stadium wave! It's THE WAVE, people! You can't do THE WAVE alone."},
    {"speaker": "Howie Mandel", "text": "Let's take a look at how the clues fit and find out who is taking the money."},
    {"speaker": None, "text": "Clue 5: \"THE MOTION OF THE OCEAN IS THE NOTION.\" Waves are the motion of the ocean; doing the wave recreates a human ocean in the stadium. 1,918 got it right."},
    {"speaker": None, "text": "Clue 4: \"'NSYNC STADIUM TOUR.\" The entire stadium has to be in sync to execute the wave. 317 got it right."},
    {"speaker": None, "text": "Clue 3: \"WHAT GOES AROUND COMES AROUND.\" The wave travels all the way around the stadium and comes back to where it started. 163 got it right."},
    {"speaker": None, "text": "Clue 2: \"A STAND UP ROUTINE.\" You stand up when it's your turn — that's the routine of doing the wave. 60 got it right."},
    {"speaker": None, "text": "Clue 1: \"PEAKS AND VALLEYS.\" The wave creates peaks (when people stand) and valleys (when they sit) across the stadium. 15 got it right."},
    {"speaker": None, "text": "Gold (Clue 1): 15 winners at $200.00 each. Silver (Clue 2): 60 winners at $41.66 each. Bronze (Clue 3): 163 winners at $12.26 each."},
    {"speaker": "Howie Mandel", "text": "Congratulations to our best guessers: Boss GL, Neo Minor 3, Jazzy Annex 293, Waldo 117, and Mac and Cheese 0497!"},
]

APR30_R2_RESULTS = [
    {"speaker": "Howie Mandel", "text": "What could it be? Carl, open the ball! SPIDER-MAN! It's SPIDER-MAN!"},
    {"speaker": "Howie Mandel", "text": "Let's take a look at how the clues fit."},
    {"speaker": None, "text": "Clue 5: \"HERO FROM A COMIC BOOK KNOWN FOR HIS ARACHNID LOOK.\" Spider-Man is a Marvel comic book hero whose appearance is based on the arachnid (spider). 6,666 got it right."},
    {"speaker": None, "text": "Clue 4: \"THE MASKED SWINGER.\" Spider-Man wears a mask and swings from building to building on his webs. 2,129 got it right."},
    {"speaker": None, "text": "Clue 3: \"DIGITAL WEB DEVELOPER.\" Spider-Man uses his fingers (digits) to shoot webs, making him a digital web developer. 223 got it right."},
    {"speaker": None, "text": "Clue 2: \"A LITTLE BIT AT FIRST.\" Spider-Man's origin story begins with a small bite from a radioactive spider. 5 got it right."},
    {"speaker": None, "text": "Clue 1: \"TACKY WALL DECOR.\" Spider-Man clings to walls, making him literally like wall decor. 1 got it right."},
    {"speaker": None, "text": "Gold (Clue 1): 1 winner at $3,000.00. Silver (Clue 2): 5 winners at $500.00 each. Bronze (Clue 3): 223 winners at $8.96 each."},
    {"speaker": "Howie Mandel", "text": "One best guesser is taking $3,000 for the Gold: Gloomy Bed 90007! Our Silver winners, there are five at $500 each. There are 223 Bronze winners at $8.96 a piece."},
]

APR29_R1_RESULTS = [
    {"speaker": "Hunter March", "text": "Correct answer was: BROKEN HEART. Ah, the crystal ball got a little tricky on us today."},
    {"speaker": "Hunter March", "text": "Let's see what people said. Maybe someone got it right away. Maybe nobody got it right at all. Let's find out who's taking home the money."},
    {"speaker": None, "text": "Clue 5: \"BEYOND SAD, OH GEE, USE THE EMOJI.\" When you're beyond sad, your heart's broken, and you might use the broken heart emoji. 3,657 got it right."},
    {"speaker": None, "text": "Clue 4: \"YOUR CARDIOLOGIST CAN'T HELP YOU.\" It may feel like you need a cardiologist, but they can't actually fix a broken heart. 5,015 got it right."},
    {"speaker": None, "text": "Clue 3: \"THE PUMP BURST.\" Your heart is a pump, and burst means broken. 274 got it right."},
    {"speaker": None, "text": "Clue 2: \"LITERALLY NOT LITERAL.\" Your heart isn't literally broken, even if it does feel that way. 14 got it right."},
    {"speaker": None, "text": "Clue 1: \"NOT A HAPPY ENDING.\" If you have a broken heart, usually that's not from the happiest of endings. 3 got it right."},
    {"speaker": None, "text": "Gold (Clue 1): 3 winners at $1,000.00 each. Silver (Clue 2): 14 winners at $178.57 each. Bronze (Clue 3): 274 winners at $7.30 each."},
    {"speaker": "Hunter March", "text": "I'll tell you right now, three people are having a very happy ending 'cause they got it right on clue number one. They put broken heart."},
    {"speaker": "Hunter March", "text": "Congratulations to Skillful Cabin 352, Yoda Man, and Grouchy Dad Oscar."},
    {"speaker": "Hunter March", "text": "If you guys happen to want to take a video of yourselves winning, take a screenshot of your phone, post it to your socials. We'd love to congratulate you."},
    {"speaker": "Hunter March", "text": "Send it to us at Netflix Games at Hunter March. With that being said, congrats to our other winners too. But hey, all about gold, baby!"},
    {"speaker": "Hunter March", "text": "Congratulations to the Puzzle One winners. It's what we love to see is a lot of winners."},
    {"speaker": "Hunter March", "text": "And we're still finding ways to thank our fans. So we're putting even more prizes into the mix."},
    {"speaker": "Hunter March", "text": "As you guys know, everyone who answers correctly on our second puzzle is taking home one of these: the K-pop Demon Hunters glass from the Netflix shop. It's worth $24.95."},
    {"speaker": "Hunter March", "text": "Pretty sweet. All you have to do is pay for shipping. And you don't have to win money to win the glass."},
    {"speaker": "Hunter March", "text": "You just have to give us a correct answer by clue five on this next puzzle and it's all yours."},
    {"speaker": "Hunter March", "text": "Friendly reminder too, by the way: redeem your vouchers. I know life gets busy, but these vouchers do expire."},
]

APR29_R2_RESULTS = [
    {"speaker": "Hunter March", "text": "Correct answer was: TAMBOURINE."},
    {"speaker": "Hunter March", "text": "That's right, baby! It's tambourine! And when they cut back to me, you're not going to believe what I got. More tambourine!"},
    {"speaker": "Hunter March", "text": "Let's take a look at how the clues fit. Find out who's taking home the money."},
    {"speaker": None, "text": "Clue 5: \"AN INSTRUMENT THAT IS MOSTLY CYMBALIC.\" It is a percussion instrument with strong cymbal vibes. 2,562 got it right."},
    {"speaker": None, "text": "Clue 4: \"OFTEN USED BY HIPPIES.\" You often smack them against your hip as the way to play that instrument. 628 got it right."},
    {"speaker": None, "text": "Clue 3: \"SLAP-HAPPY.\" Slapping the tambourine creates joyful music. 124 got it right."},
    {"speaker": None, "text": "Clue 2: \"ROUND AND ROUND.\" Tambourines are round, and so are the jingles in them. 66 got it right."},
    {"speaker": None, "text": "Clue 1: \"A FIRM HANDSHAKE.\" You grip the tambourine firmly in your hand and you shake it. 5 got it right."},
    {"speaker": None, "text": "Gold (Clue 1): 5 winners at $600.00 each. Silver (Clue 2): 66 winners at $37.00 each. Bronze (Clue 3): 124 winners at $16.00 each."},
    {"speaker": "Hunter March", "text": "Congratulations to Positive duo, Big book fam, Bigwig Bree, Sneet 25, and to all silver and bronze winners."},
    {"speaker": "Hunter March", "text": "Congratulations to everybody! And if you got it right, of course, go get your voucher."},
]

with open("data/transcripts.json") as f:
    transcripts = json.load(f)

for entry in transcripts:
    if entry["date"] == "Thursday, April 30, 2026":
        for s in entry["sections"]:
            if s["tag"] == "Round 1 Results":
                s["lines"] = APR30_R1_RESULTS
            elif s["tag"] == "Round 2 Results":
                s["lines"] = APR30_R2_RESULTS
    elif entry["date"] == "Wednesday, April 29, 2026":
        for s in entry["sections"]:
            if s["tag"] == "Round 1 Results":
                s["lines"] = APR29_R1_RESULTS
            elif s["tag"] == "Round 2 Results":
                s["lines"] = APR29_R2_RESULTS

with open("data/transcripts.json", "w") as f:
    json.dump(transcripts, f, indent=2)
    f.write("\n")
print("Done.")
