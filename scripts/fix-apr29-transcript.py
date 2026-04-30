#!/usr/bin/env python3
"""One-off script: expand April 29 transcript to verbatim and update auto-import prompt."""
import json

VERBATIM_SECTIONS = [
    {
        "tag": "Intro",
        "lines": [
            {"speaker": "Hunter March", "text": "Welcome to Best Guess Live! Hello, how we doing? I'm your host, Hunter March."},
            {"speaker": "Hunter March", "text": "This show, if you guys didn't know, is a partnership. I bring the clues, you bring the guesses, Netflix is financing."},
            {"speaker": "Hunter March", "text": "Thank you guys so much, really appreciate it. For the guessers and for me, it's basically a heist movie. The only thing is you guys get to keep the money."},
            {"speaker": "Hunter March", "text": "And tonight, $15,000 is in play. Here's the planners—we call it the rules."},
            {"speaker": "Hunter March", "text": "Each episode of Best Guess Live has two rounds. Each round has one puzzle. Each puzzle has three sets of winners: gold, silver, and bronze."},
            {"speaker": "Hunter March", "text": "Before each round, we're going to load our crystal ball with a secret item. Now it could be anything, anything."},
            {"speaker": "Hunter March", "text": "Then I'll give you five clues. But remember, the clues are written like riddles. They're meant to make you think."},
            {"speaker": "Hunter March", "text": "After each clue, you get 20 seconds to submit an answer, but you only get one best guess per round. Not one per clue, one per round."},
            {"speaker": "Hunter March", "text": "So make sure you're confident before you lock it in. It has to be the exact answer, and we don't accept typos."},
            {"speaker": "Hunter March", "text": "Bottom line: you want to be fast, but you have to be right."},
            {"speaker": "Hunter March", "text": "Everyone that locks in a correct answer on the earliest clue will split the gold prize pot of $3,000."},
            {"speaker": "Hunter March", "text": "Everyone that locks in a correct answer on the second earliest clue will split the silver pot of $2,500."},
            {"speaker": "Hunter March", "text": "And everyone that gets it right on the third earliest clue will split the bronze pot of $2,000."},
            {"speaker": "Hunter March", "text": "If you give a correct answer on one of the three earliest clues, you win."},
            {"speaker": "Hunter March", "text": "And if you're the only one to give a correct answer on one of those clues, you take the whole pot for that medal."},
            {"speaker": "Hunter March", "text": "Don't forget, if possible, take a video of you and your friends playing Best Guess Live. Send it to us or post it to your socials with the hashtag #BestGuessLive."},
            {"speaker": "Hunter March", "text": "And with all that being said, let's win some money!"}
        ]
    },
    {
        "tag": "Round 1",
        "lines": [
            {"speaker": "Hunter March", "text": "Round one is worth $7,500. Let's load the crystal ball."},
            {"speaker": "Hunter March", "text": "Okay, $7,500. That's a lot of money. It's a lot of Wednesday money. Let's look at our first clue: NOT A HAPPY ENDING."},
            {"speaker": "Hunter March", "text": "20 seconds on the clock starts now. NOT A HAPPY ENDING. That's clue one."},
            {"speaker": "Hunter March", "text": "By the way, if you guys are new here tonight, that's your first clue of five that you get for this puzzle. Then there's another one right after."},
            {"speaker": "Hunter March", "text": "If you're not new here—if you're \"old\" here, doesn't sound right, but if you're old here, hey, thanks for coming back. Really appreciate it."},
            {"speaker": "Hunter March", "text": "Time's up. NOT A HAPPY ENDING. Uncle Scorpion put Happy Gilmore. CCP Upins put Bambi. True, that's very true."},
            {"speaker": "Hunter March", "text": "Okay, clue number two: LITERALLY NOT LITERAL. 20 seconds on the clock starts now."},
            {"speaker": "Hunter March", "text": "NOT A HAPPY ENDING, LITERALLY NOT LITERAL. Okay. Could be a lot of things. Bambi was literally not literal. Can't imagine that's the answer."},
            {"speaker": "Hunter March", "text": "Time's up. Clue number two: LITERALLY NOT LITERAL. One and done 452 put audiobook. Okay, we got some real nerds playing tonight."},
            {"speaker": "Hunter March", "text": "Um, let's move on to clue number three: THE PUMP BURST. 20 seconds on the clock starts now."},
            {"speaker": "Hunter March", "text": "Oh, it throws a little bit of a wrench in it for me. Okay. NOT A HAPPY ENDING, LITERALLY NOT LITERAL, THE PUMP BURST."},
            {"speaker": "Hunter March", "text": "Okay, 8 seconds left. Good luck. 3, 2, 1. Time's up."},
            {"speaker": "Hunter March", "text": "Okay, THE PUMP BURST. Louis Bug from Houston, Texas put ember. Flashing carton 863 put Smashing Pumpkins."},
            {"speaker": "Hunter March", "text": "Is there a Smashing Pumpkins song I'm unaware of? The pumpkin burst? Got it. I'm feeling like a fool tonight. You guys could be way onto something I'm not."},
            {"speaker": "Hunter March", "text": "Okay, clue number four: YOUR CARDIOLOGIST CAN'T HELP YOU. 20 seconds starts now."},
            {"speaker": "Hunter March", "text": "YOUR CARDIOLOGIST CAN'T HELP YOU. Okay. Clue number four. Usually, some people have figured it out around here."},
            {"speaker": "Hunter March", "text": "A lot of people are getting it around here. Some people get it sooner, people rarely get it later, but it happens."},
            {"speaker": "Hunter March", "text": "5 seconds. Time is up. Okay, YOUR CARDIOLOGIST CAN'T HELP YOU. Chilly long snout puts sprinkler. True."},
            {"speaker": "Hunter March", "text": "And if he did, you'd be overpaying. Very scary Maryanne put the Tin Man. Your cardiologist can't help you because he doesn't have a heart. That's a great guess."},
            {"speaker": "Hunter March", "text": "Is it correct? Though we got one more clue for this first puzzle. And that clue is: BEYOND SAD, OH GEE, USE THE EMOJI."},
            {"speaker": "Hunter March", "text": "Okay, 20 seconds. We really wanted the rhyme there. 20 seconds starts now. BEYOND SAD, OH GEE, USE THE EMOJI."},
            {"speaker": "Hunter March", "text": "Okay, let's go over all the clues one more time together, people. NOT A HAPPY ENDING, LITERALLY NOT LITERAL, THE PUMP BURST, YOUR CARDIOLOGIST CAN'T HELP YOU, BEYOND SAD, OH GEE, USE THE EMOJI."},
            {"speaker": "Hunter March", "text": "Time's up. Okay, five clues down. Let's find out what's inside the crystal ball for this first puzzle."}
        ]
    },
    {
        "tag": "Round 1 Results",
        "lines": [
            {"speaker": "Hunter March", "text": "Correct answer was: BROKEN HEART. Ah, the crystal ball got a little tricky on us today."},
            {"speaker": "Hunter March", "text": "Let's see what people said. Maybe someone got it right away. Maybe nobody got it right at all. Let's find out who's taking home the money."},
            {"speaker": "Hunter March", "text": "Clue number five: BEYOND SAD, OH GEE, USE THE EMOJI. 6,668 guesses. Use the broken heart emoji when you're sad. 3,657 people got it right."},
            {"speaker": "Hunter March", "text": "Okay, clue number four: YOUR CARDIOLOGIST CAN'T HELP YOU. They can't actually fix a broken heart. 12,120 people guessed, 5,015 got it right. Well done."},
            {"speaker": "Hunter March", "text": "Okay, clue number three: THE PUMP BURST. Your heart is a pump. Burst means broken. 4,878 guesses, 274 got it right."},
            {"speaker": "Hunter March", "text": "Okay, that means clue number three is in gold position. It comes down to clues number two and one."},
            {"speaker": "Hunter March", "text": "Clue number two was LITERALLY NOT LITERAL. Your heart isn't literally broken. 3,416 people guessed, 14 people got it right. Which means they're now in gold position."},
            {"speaker": "Hunter March", "text": "And it comes down to clue number one, which is NOT A HAPPY ENDING. 2,770 guesses on clue number one."},
            {"speaker": "Hunter March", "text": "I'll tell you right now, three people are having a very happy ending 'cause they got it right on clue number one. They put broken heart."},
            {"speaker": "Hunter March", "text": "Congratulations to Skillful Cabin 352, Yoda Man, and Grouchy Dad Oscar."},
            {"speaker": "Hunter March", "text": "If you guys happen to want to take a video of yourselves winning, take a screenshot of your phone, post it to your socials. We'd love to congratulate you."},
            {"speaker": "Hunter March", "text": "Send it to us at Netflix Games at Hunter March. With that being said, congrats to our other winners too. But hey, all about gold, baby!"},
            {"speaker": "Hunter March", "text": "Congratulations to the Puzzle One winners. It's what we love to see is a lot of winners."},
            {"speaker": "Hunter March", "text": "And we're still finding ways to thank our fans. So we're putting even more prizes into the mix."},
            {"speaker": "Hunter March", "text": "As you guys know, everyone who answers correctly on our second puzzle is taking home one of these: the K-pop Demon Hunters glass from the Netflix shop. It's worth $24.95."},
            {"speaker": "Hunter March", "text": "Pretty sweet. All you have to do is pay for shipping. And you don't have to win money to win the glass."},
            {"speaker": "Hunter March", "text": "You just have to give us a correct answer by clue five on this next puzzle and it's all yours."},
            {"speaker": "Hunter March", "text": "Friendly reminder too, by the way: redeem your vouchers. I know life gets busy, but these vouchers do expire."}
        ]
    },
    {
        "tag": "Round 2",
        "lines": [
            {"speaker": "Hunter March", "text": "So with that being said, let's give out some more money. Round two is worth $7,500. Prize pots are the same. Let's load the crystal ball."},
            {"speaker": "Hunter March", "text": "All right, heartbroken was the first answer. Let's turn those heartbreaks around, people. I hope you all win right now."},
            {"speaker": "Hunter March", "text": "Clue number one: A FIRM HANDSHAKE. 20 seconds on the clock starts now. A FIRM HANDSHAKE."},
            {"speaker": "Hunter March", "text": "Clue number one. You got 4 seconds left. Time is up. Ferocious five put deal. Definitely. You make a deal, you get the firm handshake."},
            {"speaker": "Hunter March", "text": "Nightwing five said Superman. One of the firmest handshakes—has been known to kill people with his handshake."},
            {"speaker": "Hunter March", "text": "Guys, these are good guesses. Are they going to hold for clue number two? Clue number two is ROUND AND ROUND. 20 seconds starts now."},
            {"speaker": "Hunter March", "text": "All right, ROUND AND ROUND. Handshake? ROUND AND ROUND. 10 seconds left. 3, 2, 1. Time's up."},
            {"speaker": "Hunter March", "text": "We've got ROUND AND ROUND. Jerry the King put binoculars. I mean yeah, just by shape for sure."},
            {"speaker": "Hunter March", "text": "And then Kenny Marie said a blender, which definitely goes around and round."},
            {"speaker": "Hunter March", "text": "Okay, clue number three: SLAP-HAPPY. 20 seconds on the clock starts now."},
            {"speaker": "Hunter March", "text": "We've got A FIRM HANDSHAKE, ROUND AND ROUND, SLAP-HAPPY. 10 seconds. SLAP-HAPPY with a hyphen in the middle."},
            {"speaker": "Hunter March", "text": "Does the hyphen have anything to do with it? I genuinely don't. Time's up."},
            {"speaker": "Hunter March", "text": "SLAP-HAPPY. Phoenix to Phoenix said Ring around the Rosie. Red gum 904 put electric bass. Definitely. That's a good guess."},
            {"speaker": "Hunter March", "text": "Clue number four might enlighten us. Clue number four is OFTEN USED BY HIPPIES. 20 seconds on the clock starts now."},
            {"speaker": "Hunter March", "text": "There's a lot of things often used by hippies that do make them slap happy. But are they the correct answer? 5 seconds left."},
            {"speaker": "Hunter March", "text": "SLAP-HAPPY often gets used by hippies. Time's up. Silver 107 from Chicago, Illinois said peace. Yeah, those hippies, they'll really use that."},
            {"speaker": "Hunter March", "text": "Delightful train 673 said the word \"groovy.\" I think you could have just put groovy, but I like that you added \"the word.\""},
            {"speaker": "Hunter March", "text": "Okay, here's your fifth and final clue. Again, your last chance to get your voucher for this week."},
            {"speaker": "Hunter March", "text": "Clue five: AN INSTRUMENT THAT IS MOSTLY CYMBALIC. Oh, interesting spelling. 20 seconds on the clock starts now."},
            {"speaker": "Hunter March", "text": "Oh, hey, interesting spelling. Oh, hey. Did we make a mistake or is that interesting spelling?"},
            {"speaker": "Hunter March", "text": "Isn't it crazy? Oh my god, I was looking at \"instrument\" the whole time. I thought \"instrument\" was spelled wrong. My bad, I'm an idiot."},
            {"speaker": "Hunter March", "text": "All right, time's up. That's clue number five. Let's find out what's been inside the crystal ball."}
        ]
    },
    {
        "tag": "Round 2 Results",
        "lines": [
            {"speaker": "Hunter March", "text": "Correct answer was: TAMBOURINE."},
            {"speaker": "Hunter March", "text": "That's right, baby! It's tambourine! And when they cut back to me, you're not going to believe what I got. More tambourine!"},
            {"speaker": "Hunter March", "text": "Let's take a look at how the clues fit. Find out who's taking home the money."},
            {"speaker": "Hunter March", "text": "AN INSTRUMENT THAT IS MOSTLY CYMBALIC. It is a percussion instrument with strong cymbal vibes. Lots of little symbolicness in there. 7,985 guesses, 2,562 got it right. Well done. Hey, a third of the people got it right. It's still impressive."},
            {"speaker": "Hunter March", "text": "Clue number four: OFTEN USED BY HIPPIES. Well, you often smack them against your hip as the way to play that instrument. Also, I do feel like they are often used by hippies. I have no evidence of that, but it just feels right. 4,619 guesses, 628 people got it right."},
            {"speaker": "Hunter March", "text": "Okay, clue number three: SLAP-HAPPY. Slapping the tambourine creates joyful music to some. 7,362 guesses, 124 got it right."},
            {"speaker": "Hunter March", "text": "Okay, clue number two: ROUND AND ROUND. Tambourines are round, and so are the jingles in them. It's round and round. 7,156 guesses, 66 got it right."},
            {"speaker": "Hunter March", "text": "Let's move on to clue number one: A FIRM HANDSHAKE. It's because you grip the tambourine firmly in your hand and you shake it. 5,300 guesses on clue number one. I'll tell you right now, clue number one is in gold position with five correct guesses. Meaning those five people are going home with $600 each."},
            {"speaker": "Hunter March", "text": "Congratulations to Positive duo, Big book fam, Big wig brie, Sne—of course we got our silvers, 66 people winning $37 each. 124 bronze winners winning $16 each."},
            {"speaker": "Hunter March", "text": "Congratulations to everybody! And if you got it right, of course, go get your voucher."}
        ]
    },
    {
        "tag": "Outro",
        "lines": [
            {"speaker": "Hunter March", "text": "That is it for this episode of Best Guess Live. Congratulations to all of our winners, including everyone who picked up a voucher for the K-pop Demon Hunter glass."},
            {"speaker": "Hunter March", "text": "If you didn't grab one tonight, come back tomorrow for another chance, and jump in the Discord and say hi. I'll be reading."},
            {"speaker": "Hunter March", "text": "We're here every weekday at 8 Eastern, 5 Pacific. Bye-bye!"},
            {"speaker": None, "text": "MOST SUBMITTED WRONG GUESSES: Puzzle 1: HEART ATTACK, DIVORCE, CRYING, DEATH, HEART"},
            {"speaker": None, "text": "Puzzle 2: CYMBALS, PEACE SIGN, HIGH FIVE, BOXING, ARM WRESTLING"}
        ]
    }
]

with open("data/transcripts.json") as f:
    transcripts = json.load(f)

for entry in transcripts:
    if entry.get("date") == "Wednesday, April 29, 2026":
        entry["sections"] = VERBATIM_SECTIONS
        break

with open("data/transcripts.json", "w") as f:
    json.dump(transcripts, f, indent=2)
    f.write("\n")

print("Done.")
