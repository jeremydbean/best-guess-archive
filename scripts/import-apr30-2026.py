#!/usr/bin/env python3
"""One-off import: Thursday April 30 2026 — THE WAVE / SPIDER-MAN"""
import json, subprocess, sys

DATE = "Thursday, April 30, 2026"
HOST = "Howie Mandel"

GAMES = [
    {
        "date": DATE, "pot": 7500, "format": "v2", "host": HOST,
        "secretItem": "THE WAVE",
        "clues": [
            {"text": "PEAKS AND VALLEYS",                    "correct": "15",    "guesses": "6,341", "explanation": "The wave creates peaks (when people stand) and valleys (when they sit) across the stadium."},
            {"text": "A STAND UP ROUTINE",                   "correct": "60",    "guesses": "4,944", "explanation": "You stand up when it's your turn — that's the routine of doing the wave."},
            {"text": "WHAT GOES AROUND COMES AROUND",        "correct": "163",   "guesses": "8,569", "explanation": "The wave travels all the way around the stadium and comes back to where it started."},
            {"text": "'NSYNC STADIUM TOUR",                  "correct": "317",   "guesses": "3,162", "explanation": "The entire stadium has to be in sync to execute the wave."},
            {"text": "THE MOTION OF THE OCEAN IS THE NOTION","correct": "1,918", "guesses": "6,870", "explanation": "Waves are the motion of the ocean; doing the wave recreates a human ocean in the stadium."},
        ],
        "goldClue": 1, "silverClue": 2, "bronzeClue": 3,
        "goldWinners": 15, "silverWinners": 60, "bronzeWinners": 163,
        "totalWinners": 238,
        "goldPayout": 200, "silverPayout": 41.66, "bronzePayout": 12.26,
        "winnerPayout": "$7,500.00",
        "winnerNames": "Boss GL, Neo Minor 3, Jazzy Annex 293, Waldo 117, Mac and Cheese 0497",
        "wrongGuesses": "WAVES, JUSTIN TIMBERLAKE, STOCK MARKET, ROLLER COASTER, CAROUSEL",
    },
    {
        "date": DATE, "pot": 7500, "format": "v2", "host": HOST,
        "secretItem": "SPIDER-MAN",
        "clues": [
            {"text": "TACKY WALL DECOR",                                    "correct": "1",     "guesses": "6,730", "explanation": "Spider-Man clings to walls, making him literally like wall decor."},
            {"text": "A LITTLE BITE AT FIRST",                              "correct": "5",     "guesses": "5,531", "explanation": "Spider-Man's origin story begins with a small bite from a radioactive spider."},
            {"text": "DIGITAL WEB DEVELOPER",                               "correct": "223",   "guesses": "6,560", "explanation": "Spider-Man uses his fingers (digits) to shoot webs, making him a digital web developer."},
            {"text": "THE MASKED SWINGER",                                  "correct": "2,129", "guesses": "5,210", "explanation": "Spider-Man wears a mask and swings from building to building on his webs."},
            {"text": "HERO FROM A COMIC BOOK KNOWN FOR HIS ARACHNID LOOK", "correct": "6,666", "guesses": "7,753", "explanation": "Spider-Man is a Marvel comic book hero whose appearance is based on the arachnid (spider)."},
        ],
        "goldClue": 1, "silverClue": 2, "bronzeClue": 3,
        "goldWinners": 1, "silverWinners": 5, "bronzeWinners": 223,
        "totalWinners": 229,
        "goldPayout": 3000, "silverPayout": 500, "bronzePayout": 8.96,
        "winnerPayout": "$7,500.00",
        "winnerNames": "Gloomy Bed 90007",
        "wrongGuesses": "WALLPAPER, SPIDER, SPIDER WEB, POSTER, WALL PAPER",
        "bonus": {
            "title": "K-Pop Demon Hunters Glass",
            "desc": "Everyone who answers correctly on the second puzzle, on any clue, will receive a voucher for a K-Pop Demon Hunters glass from the Netflix Shop, worth $24.95. The winner only needs to pay for shipping.",
        },
    },
]

TRANSCRIPT = {
    "date": DATE,
    "host": HOST,
    "secretItems": ["THE WAVE", "SPIDER-MAN"],
    "rounds": [
        {"round": 1, "secretItem": "THE WAVE",    "host": HOST, "pot": 7500, "format": "v2",
         "clues": ["PEAKS AND VALLEYS", "A STAND UP ROUTINE", "WHAT GOES AROUND COMES AROUND", "'NSYNC STADIUM TOUR", "THE MOTION OF THE OCEAN IS THE NOTION"]},
        {"round": 2, "secretItem": "SPIDER-MAN",  "host": HOST, "pot": 7500, "format": "v2",
         "clues": ["TACKY WALL DECOR", "A LITTLE BITE AT FIRST", "DIGITAL WEB DEVELOPER", "THE MASKED SWINGER", "HERO FROM A COMIC BOOK KNOWN FOR HIS ARACHNID LOOK"]},
    ],
    "sections": [
        {
            "tag": "Intro",
            "lines": [
                {"speaker": "Howie Mandel", "text": "Welcome to Best Guess Live! I'm your host, Howie Mandel. I have to say, I'm welcoming... we have a streak, a player streak from Mama of Three Crazies. This is your fourth time in a row playing! And Ancient Storm 257, you've returned 16 times! This is addictive. And we got some new players too, but start a streak!"},
                {"speaker": "Howie Mandel", "text": "I want to tell you something; I'm giving you a little BTS, behind the scenes. Our artisanal clues are meticulously picked by a team of puzzle makers, aged for five years in a climate-controlled oak barrel, and then decanted for 90 minutes. And tonight's clues have a hint of cedar with a touch of vanilla with a heavy finish of $15,000!"},
                {"speaker": "Howie Mandel", "text": "In the world of clues, I'm a sommelier. Okay, so let's pour out a nice glass of rules."},
                {"speaker": "Howie Mandel", "text": "Each episode of Best Guess Live has two rounds. Each round has one puzzle. Each puzzle has three sets of winners: Gold, Silver, and Bronze. Before each round, we're going to load our crystal ball with a secret item. It could be absolutely anything. Then I'm going to give you five clues. But remember, the clues—they're riddles, people! They're meant to make you think."},
                {"speaker": "Howie Mandel", "text": "After each clue, you get 20 seconds to submit an answer. But you only get one best guess per round—not one per clue, one per round. So make sure you're confident before you lock it in. It's got to be the exact answer, and we're not going to accept typos. Bottom line: you want to be fast, but you have to be right."},
                {"speaker": "Howie Mandel", "text": "Everyone that locks in a correct answer on the earliest clue will split the Gold prize pot of $3,000. Everyone that locks in a correct answer on the second earliest clue will split the Silver pot of $2,500. And everyone that gets it on the third earliest clue will split the Bronze pot of $2,000."},
                {"speaker": "Howie Mandel", "text": "So, if you give a correct answer on one of the three earliest clues, you will win. And if you're the only one to give a correct answer on one of those clues, you take the whole pot for that medal."},
                {"speaker": "Howie Mandel", "text": "Don't forget, if possible, take a video of you and your friends or family playing Best Guess Live and send it to us or post it on your socials with #BestGuessLive. Enough talk! Let's win some money. Round 1 is worth $7,500. Load that crystal ball right now!"},
            ]
        },
        {
            "tag": "Round 1",
            "lines": [
                {"speaker": "Howie Mandel", "text": "All right, we're about to find out what is in the crystal ball. You know how we do that; I give you clues. I'm going to start with the first clue: PEAKS AND VALLEYS. 20 seconds on the clock right now."},
                {"speaker": "Howie Mandel", "text": "The clock is counting down. Remember, the earlier you get it right, the better chance you have of winning more money. All right, answers are coming in. People are taking a shot. We have almost 15 guesses just on this first clue. Time is up!"},
                {"speaker": "Howie Mandel", "text": "Somebody said \"High School.\" Those are PEAKS AND VALLEYS; things were up and down. For me, it was one long valley that I never finished or got through."},
                {"speaker": "Howie Mandel", "text": "Here's your second clue: A STAND UP ROUTINE. The clock starts now. 20 seconds. 6,300 people guessed on that first one."},
                {"speaker": "Howie Mandel", "text": "With 5 seconds left on the clock, guesses are coming in. Scarlet Wizard 31 said \"Airline Food.\" About A Win 67 said \"Surfing.\" That makes sense. What's the deal with... oh, STAND UP ROUTINE, \"What's the deal?\" Thank you. Apparently, I'm the only one in the room that's closed-captioned."},
                {"speaker": "Howie Mandel", "text": "Here's your third clue: WHAT GOES AROUND COMES AROUND. The clock starts now. 20 seconds on the clock. We already have over 11,000 guesses in and counting. Over 30,000 players are right here. Time is up!"},
                {"speaker": "Howie Mandel", "text": "Yummy Waffle said \"Karma.\" Prickly Table said \"The Flu,\" which is ultimately the best STAND UP ROUTINE anybody can do."},
                {"speaker": "Howie Mandel", "text": "Here's your fourth clue: 'NSYNC STADIUM TOUR. The clock starts now. 5 seconds left on the clock. Over 20,000 submitted guesses already. Spiffy Queen 83 said \"The Moon.\" Sprinkled Mountain 50 said \"Super Bowl Halftime Show.\""},
                {"speaker": "Howie Mandel", "text": "Final clue! Your fifth clue: THE MOTION OF THE OCEAN IS THE NOTION. The clock starts now. 3 seconds, 2 seconds, 1 second. Time is up! And we have almost 30,000 submitted guesses on this first round for $7,500. Let us find out what is in that crystal ball."},
            ]
        },
        {
            "tag": "Round 1 Results",
            "lines": [
                {"speaker": "Howie Mandel", "text": "Open that ball right now! THE WAVE! The stadium wave! It's THE WAVE, people! You can't do THE WAVE alone."},
                {"speaker": "Howie Mandel", "text": "Let's take a look at how the clues fit and find out who is taking the money."},
                {"speaker": "Howie Mandel", "text": "The fifth clue was THE MOTION OF THE OCEAN IS THE NOTION. Waves are the motion of the ocean; we're trying to create a human ocean when we do THE WAVE at a stadium. 6,870 of you guessed; 1,918 of you got the best guess right."},
                {"speaker": "Howie Mandel", "text": "Clue 4 was 'NSYNC STADIUM TOUR. The entire stadium, you got to be in sync. 3,162 of you thought you had the proper guess; 317 of you got that correct."},
                {"speaker": "Howie Mandel", "text": "Clue 3: WHAT GOES AROUND COMES AROUND. Self-explanatory! THE WAVE makes its way around the entire stadium and then back to you. 8,569 guesses; 163 of you got it correct."},
                {"speaker": "Howie Mandel", "text": "Clue 2: A STAND UP ROUTINE. You stand up when it's your turn. That's how you make THE WAVE. 4,944 guesses on that one; 60 of you got it correct."},
                {"speaker": "Howie Mandel", "text": "Clue 1 was PEAKS AND VALLEYS. THE WAVE creates highs and lows. 6,341 guesses on that first clue. You know what? 15 people got it correct! That is the Gold. 15 people are each splitting $3,000, so $200 each. The Silver people, 60 of you, are getting $41.66. And on the Bronze, 163 people are splitting $12.26."},
                {"speaker": "Howie Mandel", "text": "Congratulations to our best guessers: Boss GL, Neo Minor 3, Jazzy Annex 293, Waldo 117, and Mac and Cheese 0497!"},
            ]
        },
        {
            "tag": "Round 2",
            "lines": [
                {"speaker": "Howie Mandel", "text": "It's day four of our giveaway of the K-pop Demon Hunters glass from the Netflix Shop. Everyone who answers correctly on our second puzzle coming up is getting this for free."},
                {"speaker": "Howie Mandel", "text": "One last thing: Rob on Discord wants us to wish his wife Amber a happy birthday. No! Rob, I think you should go out and do something nice for her; don't rely on us. But this next game is in honor of Amber's birthday."},
                {"speaker": "Howie Mandel", "text": "Round 2, where $7,500 is up for grabs! Load that crystal ball. Here's your first clue: TACKY WALL DECOR. The clock starts now. What could it be?"},
                {"speaker": "Howie Mandel", "text": "5 seconds left. Frojo Joe 6000 said \"Big Mouth Billy Bass.\" You know, I have one of those. Is that TACKY WALL DECOR? My wife loves it."},
                {"speaker": "Howie Mandel", "text": "Here's the second clue: A LITTLE BITE AT FIRST. The clock starts now. We already have over 7,000 submitted answers. Almost 32,000 people playing right now. Time is up!"},
                {"speaker": "Howie Mandel", "text": "Sulky Cactus 101 says \"Appetizers.\" Super Dupe 22 said \"Glue.\""},
                {"speaker": "Howie Mandel", "text": "Clue 3: DIGITAL WEB DEVELOPER. The clock starts now. 10 seconds left. Guesses are streaming in faster than I could even think of. Rowdy Scooby 94 said \"GoDaddy.\""},
                {"speaker": "Howie Mandel", "text": "Here is clue 4: THE MASKED SWINGER. Clock starts now. I think that one gives it away. 2 seconds left. Time is up. Harry Martian said \"Darth Vader.\""},
                {"speaker": "Howie Mandel", "text": "Final clue! Final chance to guess! HERO FROM A COMIC BOOK KNOWN FOR HIS ARACHNID LOOK. Clock starts now. Put in a guess, people, because you could win that Netflix cup! Time is up. 6,000 guesses on that last one. Mary Nearer 389 says \"Zorro.\""},
            ]
        },
        {
            "tag": "Round 2 Results",
            "lines": [
                {"speaker": "Howie Mandel", "text": "What could it be? Carl, open the ball! SPIDER-MAN! It's SPIDER-MAN!"},
                {"speaker": "Howie Mandel", "text": "Let's take a look at how the clues fit."},
                {"speaker": "Howie Mandel", "text": "Clue 5 was HERO FROM A COMIC BOOK KNOWN FOR HIS ARACHNID LOOK. That is SPIDER-MAN. 7,753 guesses; 6,666 got it correct."},
                {"speaker": "Howie Mandel", "text": "Clue 4: THE MASKED SWINGER. SPIDER-MAN wears a mask and swings from building to building. 5,210 of you guessed; 2,129 guessed right."},
                {"speaker": "Howie Mandel", "text": "Clue 3: DIGITAL WEB DEVELOPER. When SPIDER-MAN makes webs, he makes the gesture with his fingers. 6,560 of you guessed; 223 guessed correctly."},
                {"speaker": "Howie Mandel", "text": "Clue 2: A LITTLE BITE AT FIRST. Getting that little bite by that little spider starts the story. 5,531 of you guessed; five of you got it correct."},
                {"speaker": "Howie Mandel", "text": "Clue 1: TACKY WALL DECOR. SPIDER-MAN hangs on walls; he sticks to the walls. He is like wall decor there! 6,730 people took a first guess. Only ONE of you got it correct!"},
                {"speaker": "Howie Mandel", "text": "One best guesser is taking $3,000 for the Gold: Gloomy Bed 90007! Our Silver winners, there are five at $500 each. There are 223 Bronze winners at $8.96 a piece."},
            ]
        },
        {
            "tag": "Outro",
            "lines": [
                {"speaker": "Howie Mandel", "text": "That's it for this episode! Congratulations to all of our winners, including everyone who picked up a voucher for the K-pop Demon Hunters glass. Come back tomorrow and bring your best guess!"},
                {"speaker": None, "text": "MOST SUBMITTED WRONG GUESSES: Puzzle 1: WAVES, JUSTIN TIMBERLAKE, STOCK MARKET, ROLLER COASTER, CAROUSEL"},
                {"speaker": None, "text": "Puzzle 2: WALLPAPER, SPIDER, SPIDER WEB, POSTER, WALL PAPER"},
            ]
        },
    ]
}


def main():
    with open("data/games.json") as f:
        games = json.load(f)
    with open("data/transcripts.json") as f:
        transcripts = json.load(f)

    existing_keys = {(g["date"], g.get("secretItem")) for g in games}
    new_games = [g for g in GAMES if (g["date"], g.get("secretItem")) not in existing_keys]
    if new_games:
        games.extend(new_games)
        with open("data/games.json", "w") as f:
            json.dump(games, f, indent=2)
            f.write("\n")
        print(f"Added {len(new_games)} game(s).")
    else:
        print("Games already present — skipped.")

    existing_dates = {t["date"] for t in transcripts}
    if DATE not in existing_dates:
        transcripts.append(TRANSCRIPT)
        with open("data/transcripts.json", "w") as f:
            json.dump(transcripts, f, indent=2)
            f.write("\n")
        print("Transcript added.")
    else:
        print("Transcript already present — skipped.")

    result = subprocess.run(["node", "tools/audit-data.mjs", "--fix"], capture_output=True, text=True)
    print(result.stdout.strip())
    result2 = subprocess.run(["node", "tools/audit-data.mjs"], capture_output=True, text=True)
    print(result2.stdout.strip())
    if result2.returncode != 0:
        print(result2.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
