"""
This file is required by KBC game if SQL isn't installed
"""

import random      #for randomizing question selection

err = "SQL not installed."
database = []
topics = []
with open("./topics/LIST_OF_TOPICS.txt") as f1:
  topics = f1.read().split("\n")
  for i in topics:
    with open("./topics/%s.txt" % i) as f2:
      database += f2.read().split("\n")
database = [
    eval(i[:-1] if i.endswith(",") else i) for i in database
    if not i.startswith("INSERT") and not i.startswith(";")
]

#fetches a random question based on topic and level
def qdata(level, topic):
  return random.choice([i for i in database if i[6] == level and i[7] == topic])

#fetches list of topics
def gettopics():
  return [(i, 0) for i in topics]

#fetches question count
def numq():
  return len(database)

import base64
devs = base64.b64decode("ICAgU09IQU0gUFJFTSBLQVJUSElLJ1MgIA==").decode("ascii")

#following functions are just to avoid errors_________________________________
def addquestion(*x, **y):
  return err

def addscore(*x, **y):
  print(err)

def printhighscores(*x, **y):
  print(err)

def printhistory():
  print(err)

def sqldirect():
  print(err)

def close():
  return ""

if __name__ == "__main__":
  input("If you want to play the game, close this and open 'play_KBC_game.py'")