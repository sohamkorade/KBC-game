"""
Kaun Banega Crorepati (KBC) game in Python

# PLEASE RUN THIS PROGRAM IN A TERMINAL (COMMAND PROMPT)
# IF YOU RUN IT IN "PYTHON IDLE" THE OUTPUT MAY BE DISTORTED
# MAKE SURE YOU KEEP THE FONT SMALL TO HOLD AT LEAST 100 CHARACTERS PER LINE
"""

# display loading until the database is loaded
print("Loading Kaun Banega Crorepati...", end="\r")

from random import randint, shuffle, choice, sample
try:
  import kbcsql                        # for SQL connection
except:
  print("Can't connect to the MySQL database.\n" "Press <ENTER> to run without MySQL...\n\n")
  input()
  print("Running using alternative method. Certain features may not work.")
  import kbcsqlnotinstalled as kbcsql  # fallback

# lists to store level-related variables
worth, money, ordinals = [
    "", "das hazaar", "bees hazaar", "pachaas hazaar", "ek lakh", "do lakh", "chaar lakh",
    "aath lakh", "solah lakh", "battees lakh", "chausath lakh", "ek crore"
], [0, 10000, 20000, 50000, 100000, 200000, 400000, 800000, 1600000, 3200000, 6400000, 10000000], [
    "", "Pehla", "Doosra", "Teesra", "Chautha", "Paanchva", "Chhata", "Saatva", "Aathva", "Nava",
    "Aakhiri"
]

# functions_________________________________________________________________________________________
# wait for player to press ENTER key
def pause():
  cprint("Press <ENTER> to continue...")
  input("")
  print("\n\n")

# print center-aligned
def cprint(x, gap=True, pausenext=False):
  if gap: print()
  for i in x.split("\n"):
    print("{:^100}".format(i))
  if pausenext: pause()

# take input and return uppercase
def uinput(upper=True):
  return input(">").upper() if upper else input(">")

# display highscores
def highscores():
  while True:
    # menu to choose topic for viewing highscores
    topic = topicchooser("Which topic's high scores would you like to view?")
    if topic == "": break
    # display highscores (external function)
    kbcsql.printhighscores(topic)
    pause()

# get feedback
def feedback():
  feedbacklist = []
  for i in ("What did you like or dislike about the game? ",
            "Was there anything in the rules you didn't understand? ",
            "What would you change about the game? ", "Did you enjoy the overall game experience? ",
            "How many stars will this game get out of five? "):
    cprint(i)
    feedbacklist.append(i + uinput(0))
  cprint("Please enter your name:")
  # append feedback to log file
  try:
    with open("feedback.txt", "a") as f:
      f.write("\n%s says:\n%s\n" % (uinput(0), "\n".join(feedbacklist)))
  finally:
    cprint("Thank you for your feedback!", pausenext=1)

# display instructions
def instructions():
  cprint("Aayiye main aapko iss khel ke niyam samjhaa doon...")
  # print line by line waiting for player to press ENTER key
  with open("how_to_play.txt") as f:
    for i in f.read().split("\n"):
      print(i, end="")
      input("    ▼")

# display credits
def kbccredits():
  cprint("\n\nThis program is developed by\n")
  print("""
                                       ▄▀▀ ▄▀▄ █▄█ ▄▀▄ █▄ ▄█  
                                       ▄██ ▀▄▀ █ █ █▀█ █ ▀ █  
                                         
                                         █▀▄ █▀▄ ██▀ █▄ ▄█
                                         █▀  █▀▄ █▄▄ █ ▀ █
                                         
                                     █▄▀ ▄▀▄ █▀▄ ▀█▀ █▄█ █ █▄▀
                                     █ █ █▀█ █▀▄  █  █ █ █ █ █""")
  cprint("\nduring the 2020 coronavirus pandemic\n\n", pausenext=1)

# input question data from player and add it to database
def addquestion():
  questiondata = []
  for i in ("Question", "Option 1", "Option 2", "Option 3", "Option 4", "Correct Answer",
            "Level (1-10)", "Topic"):
    cprint(i)
    questiondata.append(uinput(0))
  cprint("Are you sure you want to add this to the main database? Y/N")
  if uinput() == "Y":
    cprint(kbcsql.addquestion(*questiondata))    # calling external function
    cprint("Add more? Y/N")
    addquestion() if uinput() != "N" else pause()
  else:
    cprint("Cancelled.")

# function to create a menu
def chooser(menu, prompt, func=False):
  cprint(prompt)
  # pretty-print ASCII table
  leftspace = " " * 31
  print("\n" + leftspace + "╔═══════════════════════════════════╗")
  print(leftspace + "║{:░^35}║".format("Choose your option"))
  print(leftspace + "╠═══════════════════════════════════╣")
  # print menu options
  for i in menu:
    if i.isdigit():
      print(leftspace + "║ {:>1} {:^28}    ║".format(i, menu[i][0] if func else menu[i]))
  # print extra option: back
  print(leftspace + "║ 0 {:>28}    ║".format("◄ Back"))
  print(leftspace + "╚═══════════════════════════════════╝")
  count = 1                  # number of invalid choices
  while True:
    count += 1
    q = uinput()
    if q in menu:            # valid choice
      return menu[q][1] if func else menu[q]
    elif q == "0":           # back
      pause()
      return ""
    elif count % 7 == 0:     # too many invalid choices
      cprint("Quitting... (Type N to cancel)")
      if uinput() != "N":
        return ""
    else:
      print("Invalid choice!")

# creates a menu to choose from topics
def topicchooser(prompt):
  topicsdict = {}
  key = 0
  # fetch topics from external function
  for i in kbcsql.gettopics():
    key += 1
    topicsdict[str(key)] = i
  return chooser(topicsdict, prompt, func=0)

# print audience poll results
def printpoll(ans, wrongoptions):
  votes = 100
  polldict = {}
  # a high percentage for correct option
  polldict[ans] = randint(45, 65)
  votes -= polldict[ans]
  for i in wrongoptions:
    polldict[i] = randint(0, votes)
    votes -= polldict[i]
  # pretty-print ASCII table
  print("\n        ╔{:═^84}╗".format(""))
  print("        ║{:^84}║".format("Poll results"))
  for i in "ABCD":
    print("        ║{:^84}║".format(""))
    print("        ║{:^3}{:<76}{:2} % ║".format(i, "▒" * polldict[i], polldict[i]))
  print("        ╚{:═^84}╝\n".format(""))
  pause()

# print prize-money cheque
def printcheque(money):
  # prints a number spread across 5 lines; each digit will be 5-character wide
  line = {}
  line[0] = "╔═══╗  ╔╗ ╔═══╗╔═══╗╔╗ ╔╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗"
  line[1] = "║╔═╗║ ╔╝║ ║╔═╗║║╔═╗║║║ ║║║╔══╝║╔══╝║╔═╗║║╔═╗║║╔═╗║║╔═╗║"
  line[2] = "║║ ║║ ╚╗║ ╚╝╔╝║╚╝╔╝║║╚═╝║║╚══╗║╚══╗╚╝╔╝║║╚═╝║║╚═╝║║║ ║║"
  line[3] = "║║ ║║  ║║ ╔═╝╔╝╔╗╚╗║╚══╗║╚══╗║║╔═╗║  ║╔╝║╔═╗║╚══╗║║║ ║║"
  line[4] = "║╚═╝║ ╔╝╚╗║ ╚═╗║╚═╝║   ║║╔══╝║║╚═╝║  ║║ ║╚═╝║╔══╝║║╚═╝║"
  line[5] = "╚═══╝ ╚══╝╚═══╝╚═══╝   ╚╝╚═══╝╚═══╝  ╚╝ ╚═══╝╚═══╝╚═══╝"
  digits = len(str(money))
  dashes = "━" * (6 * digits + 16)
  leftspace = " " * ((100 - len(dashes)) // 2)
  # top border
  print("\n%s┏%s┓" % (leftspace, dashes))
  # digits along with a border before the first and after the last digit
  for i in range(6):
    print(leftspace + "┃        ", end="")
    for j in str(money):
      print(line[i][int(j) * 5:(int(j) + 1) * 5], end=" ")
    print("        ┃")
  # bottom border
  print(leftspace + "┗%s┛\n" % dashes)

# print question and options
def kbclayout(level, q, a1, a2, a3, a4, elim="", prompt="", fillchar="▒"):
  fill = {"A": "", "B": "", "C": "", "D": ""}
  for i in elim:
    fill[i] = fillchar

  # prize-money
  print("       _______________")
  print("______╱{:^15}╲".format(money[level]))
  print("      ╲_______________╱")
  print("  {:_^100}  ".format(""))
  # question
  if len(q) <= 100:
    print("_╱{:^100.100}╲_".format(q))
  else:  # in case question is long
    for i in (q[:101], q[101:]):
      print("_╱{:^100.100}╲_".format(i))
  print(" ╲{:_^100}╱ ".format(""))

  # options
  if len(max(a1, a2, a3, a4, key=len)) > 44:     # in case options are long
    for i in (a1, a2, a3, a4):
      print("       {:_^90}".format(""))
      print("______╱{:^90.90}╲______".format(i))
      print("      ╲__{:_^88}╱".format(""))
  else:
    print("      {:_^45}  {:_^45}".format("", ""))
    print("_____╱A{:{}^44.44}╲╱B{:{}^44.44}╲_____".format(a1, fill["A"], a2, fill["B"]))
    print("     ╲_____{:_^40}╱╲_____{:_^40}╱".format("", ""))
    print("      {:_^45}  {:_^45}".format("", ""))
    print("     ╱C{:{}^44.44}╲╱D{:{}^44.44}╲_____".format(a3, fill["C"], a4, fill["D"]))
    print("     ╲_____{:_^40}╱╲_____{:_^40}╱".format("", ""))
  cprint("L = lifeline, Q = quit")
  cprint(prompt)

def congrats(level):
  print("""
          ▄▄·        ▐ ▄  ▄▄ • ▄▄▄   ▄▄▄· ▄▄▄▄▄▄• ▄▌▄▄▌   ▄▄▄· ▄▄▄▄▄▪         ▐ ▄ .▄▄ · 
          ▐█ ▌▪ ▄█▀▄ •█▌▐█▐█ ▀ ▪▀▄ █·▐█ ▀█ •██  █▪██▌██•  ▐█ ▀█ •██  ██  ▄█▀▄ •█▌▐█▐█ ▀. 
          ██ ▄▄▐█▌.▐▌▐█▐▐▌▄█ ▀█▄▐▀▀▄ ▄█▀▀█  ▐█.▪█▌▐█▌██ ▪ ▄█▀▀█  ▐█.▪▐█·▐█▌.▐▌▐█▐▐▌▄▀▀▀█▄
          ▐███▌▐█▌.▐▌██▐█▌▐█▄▪▐█▐█•█▌▐█▪ ▐▌ ▐█▌·▐█▄█▌▐█▌ ▄▐█▪ ▐▌ ▐█▌·▐█▌▐█▌.▐▌██▐█▌▐█▄▪▐█
          ·▀▀▀  ▀█▄▀▪▀▀ █▪·▀▀▀▀ .▀  ▀ ▀  ▀  ▀▀▀  ▀▀▀ .▀▀▀  ▀  ▀  ▀▀▀ ▀▀▀ ▀█▄▀▪▀▀ █▪ ▀▀▀▀ 
    """)
  cprint("'Congratulations!'")
  cprint("You have completed all the levels of this game.", pausenext=1)
  cprint("Aapko milta hai %s ka cheque!" % worth[level])
  printcheque(money[level])
  input("Kya karenge aap itne rupayon ka?\n>")
  cprint("Aap bohot umda khele. Aise hi aapki pragati hoti rahe.")
  cprint("Humare saath khelne ke liye dhanyawaad!", pausenext=1)

def talkafterquit(level):
  if level == 1:   # no money if player quits on level 1
    cprint("Dukh hota hai ki aap")
    cprint("pehle hi question pe quit kar rahe hain...")
  else:
    cprint("Badhaai ho! Aap %s rupaye jeet gaye hain!" % worth[level - 1])
    printcheque(money[level - 1])
  pause()
  cprint("Ab humein yeh khel yehi rokna hoga...")

def talkafterincorrect(level, elimoptions, ans, answer, playername):
  cprint("Yeh galat uttar hai!", pausenext=1)
  cprint("Sahi uttar yeh tha: [%s] %s" % (ans, answer), pausenext=1)
  if level == 1:                                                     # no money if player loses on level 1
    cprint("Bahut hi achha khele aap! Taaliyaan bajti rehni chaahiye...")
  else:                                                              # give cheque and end the game
    cprint("Aap jeete hain %s rupaye!" % worth[level - 1], pausenext=1)
    printcheque(money[level - 1])
    cprint("Aur yeh gaya cheque seedhe %s ji ke account mein!\n"
           "Bohot bohot badhaai ho aapko!!!" % playername)
  cprint("Mujhe behad khushi hui aapke saath khel kar.\nDhanyawad!", pausenext=1)

def asklock(q, optionsdict):
  cprint("%s Lock kar diya jaaye?? Y/N" % choice(
      ("Sure?", "Confident?", "Pakka?", "Are you confident?")))
  if uinput() != "N":                                                              #lock
    cprint("Computer %s! Option %s, '%s' par taala laga diya jaye" % (choice(
        ("Ji", "Mahashay", "Mahoday")), q, optionsdict[q]))
    pause()
    return 1
  else:                                                                            #no lock
    cprint(
        choice(("Thoda aur sochiye", "Abhi samay hai aapke paas", "Koi baat nahi",
                "Thande dimaag se sochiye", "Aaraam se", "Dhairya rakhiye")))
    return 0

def talkbeforequestion(level, breaklevel):
  # claps on level 4 and 7
  if level in (4, 7):
    print()
    cprint("*** audience claps ***")
    print()

  cprint("%s prashn %s rupayon ke liye aapke computer screen par ye raha" %
         (ordinals[level], worth[level]))
  # joke
  if breaklevel == level:
    cprint("Darshakon yahan par lenge ek chhota sa break...")
    input()
    cprint("Main toh mazaak kar raha tha!")
  pause()

def preparevariables(options, ans):
  answer = options[ans - 1]
  shuffle(options)
  optionsdict = dict(zip("ABCD", options))

  # pointing variable to correct option
  for i in optionsdict:
    if answer == optionsdict[i]:
      ans = i

  # list of wrong options
  wrongoptions = list("ABCD")
  wrongoptions.remove(ans)
  return optionsdict, options, ans, answer, wrongoptions

# main game
def startgame():
  # input player name
  cprint("Enter your name")
  # fancy text-input box
  leftspace = " " * 23
  print(leftspace, "╔══════════════════════════════════════════════════╗\n", end="")
  print(leftspace, "║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ║\r", end="")
  playername = input(leftspace + " ║ >").title()
  print(leftspace, "╚══════════════════════════════════════════════════╝\n", end="")

  # input topic for questions
  playertopic = topicchooser("On which topic would you like to take the quiz?")
  if playertopic == "": return

  cprint(
      "Toh chaliye %s ji shubh-aarambh karte hain\n"
      "iss adbhut khel ko, jiska naam hai... Kaun Banega Crorepati.\n"
      "Let's play!" % playername, pausenext=1)

  # initializing variables
  level, score, lost = 0, 0, False

  # available lifelines
  lifelines = ["Double Dip", "Audience Poll", "50:50"]

  # some random level for a joke
  breaklevel = randint(2, 8)

  # game loop
  while level < 10 and not lost:
    # updating level and score
    level += 1
    score += level * 10

    que, *options, ans, lev, topic = kbcsql.qdata(level, playertopic)
    if que == 0: return

    talkbeforequestion(level, breaklevel)

    optionsdict, options, ans, answer, wrongoptions = preparevariables(options, ans)
    q = lifeline = ""
    count = 0

    prompt = "What's your answer? (A, B, C or D)"
    kbclayout(level, que, *options, "", prompt)

    def handlelifelines():
      nonlocal elimoptions, lifeline, prompt
      if lifeline != "":               # already used lifeline for current question
        cprint("You can't use more than one lifeline for a question!\n")
        cprint("Meri taraf mat dekhiye")
        cprint("Main aapki sahaayata nahi kar paaunga!", pausenext=1)
      elif len(lifelines) < 1:         # lifeline unavailable
        cprint("Ab aapke paas koi lifeline nahi rahi!")
        cprint("Aap chaahte hain toh quit kar sakte hain.", pausenext=1)
      else:                            # lifeline available
        cprint("You have %s lifeline(s) available." % len(lifelines))
                                       # menu to choose lifeline
        lifeline = chooser(dict(zip(list("123"), lifelines)), "Choose a lifeline.")
        if lifeline == "":             # cancelled
          prompt = "L = lifeline, Q = quit"
        else:
          lifelines.remove(lifeline)
          if lifeline == "Double Dip":
            cprint("Now you have two chances to choose your answer.", pausenext=1)
            prompt = "Your first choice?"
          elif lifeline == "Audience Poll":
            printpoll(ans, wrongoptions)
          elif lifeline == "50:50":    # eliminate two random wrong options
            elim1, elim2 = sample(wrongoptions, 2)
            elimoptions = elim1 + elim2
            prompt = "%s and %s are eliminated." % (elim1, elim2)
      kbclayout(level, que, *options, elimoptions, prompt)
      return prompt, elimoptions

    elimoptions = ""
    while True:
      count += 1
      q = uinput()
      # if player chooses to quit the game or too many invalid choices
      if q == "Q" or (count % 5 == 0 and q == ""):
        cprint("Quitting... (Type N to cancel)")
        if uinput() == "N":
          kbclayout(level, que, *options, elimoptions, prompt)
        else:
          talkafterquit(level)
          lost = True
          break
      # lifeline
      if q == "L":
        prompt, elimoptions = handlelifelines()
      # cheats
      elif q == "TIKTOK":
        level = 10
        break
      elif q == "BIGB":
        break
      elif q in tuple("ABCD"):
        # in case player chooses an option that is already eliminated
        if q in tuple(elimoptions):
          print("You cannot choose", q, "now!")
        else:                                                        # valid choice
          if asklock(q, optionsdict):
            if optionsdict[q] == answer:                             # correct answer
              cprint("Bilkul sahi uttar hai aapka! %s rupaye jeet gaye aap." % worth[level])
              pause()
              break
            else:                                                    # incorrect answer
              if lifeline == "Double Dip" and elimoptions == "":     # second chance for Double Dip
                elimoptions = q
                prompt = "Your second choice?"
                kbclayout(level, que, *options, elimoptions, "Afsos! Galat jawab. " + prompt)
              else:
                elimoptions = wrongoptions
                talkafterincorrect(level, elimoptions, ans, answer, playername)
                lost = True
                break
      else:
        print("Invalid choice!")
  if level >= 10:                                                    # last level completed
    congrats(level)

# add game info to database (external function)
  kbcsql.addscore(playername, score, level, playertopic)

print(
    " " * 100, """
                                          *** ### ### ***
                                      *##                 ##*
                                  *##%s##*
                               *##                               ##*
                             *##  ╦╔═╔═╗╦ ╦╔╗╔  ╔╗ ╔═╗╔╗╔╔═╗╔═╗╔═╗ ##*
                           *##    ╠╩╗╠═╣║ ║║║║  ╠╩╗╠═╣║║║║╣ ║ ╦╠═╣   ##*
                          *##     ╩ ╩╩ ╩╚═╝╝╚╝  ╚═╝╩ ╩╝╚╝╚═╝╚═╝╩ ╩    ##*
                         *##                                           ##*
                        *##╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔════╗╔══╗##*
                        *##║╔═╗║║╔═╗║║╔═╗║║╔═╗║║╔══╝║╔═╗║║╔═╗║║╔╗╔╗║╚╣╠╝##*
                        *##║║ ╚╝║╚═╝║║║ ║║║╚═╝║║╚══╗║╚═╝║║║ ║║╚╝║║╚╝ ║║ ##*
                        *##║║ ╔╗║╔╗╔╝║║ ║║║╔╗╔╝║╔══╝║╔══╝║╚═╝║  ║║   ║║ ##*
                        *##║╚═╝║║║║╚╗║╚═╝║║║║╚╗║╚══╗║║   ║╔═╗║ ╔╝╚╗ ╔╣╠╗##*
                         *#╚═══╝╚╝╚═╝╚═══╝╚╝╚═╝╚═══╝╚╝   ╚╝ ╚╝ ╚══╝ ╚══╝##*
                          *##             ╔╗╔═╗╔══╗ ╔═══╗              ##*
                           *##            ║║║╔╝║╔╗║ ║╔═╗║             ##*
                             *##          ║╚╝╝ ║╚╝╚╗║║ ╚╝           ##*
                               *#         ║╔╗║ ║╔═╗║║║ ╔╗         ##*
                                  *##     ║║║╚╗║╚═╝║║╚═╝║      ##*
                                      *## ╚╝╚═╝╚═══╝╚═══╝  ##*
                                          *** ### ### ***
""" % kbcsql.devs)
pause()
cprint("Welcome to this brand new game!\n"
       "This game has %s questions in various topics." % kbcsql.numq())
mainmenu = {
    "1": ("Start", startgame),
    "2": ("High scores", highscores),
    "3": ("Instructions", instructions),
    "4": ("Add a question", addquestion),
    "5": ("Give feedback", feedback),
    "6": ("Credits", kbccredits),
    "7": ("Quit", kbcsql.close),            # close MySQL connection safely
    "\\SQL": (0, kbcsql.sqldirect),         # for testing
    "\\HISTORY": (0, kbcsql.printhistory)   # show all the scores
}

# main menu loop
while True:
  q = chooser(mainmenu, "What would you like to do?", func=True)
  if q != "":
    q = q()
  if q == "":
    cprint("Bye, see you soon...")
    break

input()  # ensure that last printed line is seen
