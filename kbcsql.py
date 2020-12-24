"""
This file is required by KBC game for SQL connection
"""

import mysql.connector                                                   #for SQL connection
print("Connecting to MySQL using default connection string...\n\n<ENTER> = continue, z = change")
if input().lower() == "z":
  print("Enter connection arguments:")
  db = mysql.connector.connect(host=input("host:"), user=input("user:"),
                               password=input("password:"))
else:
  db = mysql.connector.connect(host="localhost", user="root", password="root")
cur = db.cursor()
cur.execute("USE gamedb;")

#inserts question data into 'questions' table
def addquestion(que, op1, op2, op3, op4, ans, level, topic):
  try:
    sql = "INSERT INTO questions VALUES ('%s','%s','%s','%s','%s',%s,%s,'%s');"
    cur.execute(sql % (que, op1, op2, op3, op4, ans, level, topic))
    db.commit()
    return "Question added."
  except Exception as e:
    return str(e)

#insert game info into 'scores' table
def addscore(name, score, level, topic):
  sql = "INSERT INTO scores VALUES ('%s',%s,%s,'%s')"
  cur.execute(sql % (name, score, level, topic))
  db.commit()

#display highscores in a table
def printhighscores(topic, limit=5):
  sql = "SELECT name,score,level FROM scores WHERE topic='%s' ORDER BY score DESC LIMIT %s;"
  cur.execute(sql % (topic, limit))

  leftspace = " " * 16
  print(leftspace + "╔═════════════════════╦═════════════════════╦═════════════════════╗")
  print(leftspace + "║{:^21}║{:^21}║{:^21}║".format("Name", "Score", "Level"))
  print(leftspace + "╠═════════════════════╬═════════════════════╬═════════════════════╣")
  for x in cur:
    print(leftspace, end="")
    for y in x:
      print("║{:^21.21}".format(str(y)), end="")
    print("║")
  print(leftspace + "╚═════════════════════╩═════════════════════╩═════════════════════╝")

#fetches a random question based on topic and level
def qdata(level, topic):
  #error handling in case database fails to load
  try:
    sql = "SELECT * FROM questions WHERE level=%s AND topic='%s' ORDER BY RAND() LIMIT 1;"
    cur.execute(sql % (level, topic))
    return cur.fetchall()[0]
  except:
    print("Something went wrong with the database! :(")
    return (0, ) * 8

#fetches list of topics
def gettopics():
  sql = "SELECT topic FROM questions GROUP BY topic;"
  cur.execute(sql)
  return [i[0] for i in cur.fetchall()]

#fetches question count
def numq():
  cur.execute("SELECT COUNT(*) FROM questions;")
  return cur.fetchall()[0][0]

#fetches all the scores
def printhistory():
  cur.execute("SELECT * FROM scores;")
  print(*cur.fetchall(), sep="\n")

#directly send sql commands and receive output from server
def sqldirect():
  #default maximum column length
  maxcolumnlen = 15
  while True:
    try:
      print("\nQ=quit, C=commit, L=change column length")
      sql = input("enter sql>").upper()
      if sql == "Q":              #quit
        break
      elif sql == "C":            #commit
        db.commit()
      elif sql == "L":            #change column length
        try:
          maxcolumnlen = int(input("Enter column length:"))
          if maxcolumnlen < 1:    #invalid column length
            raise Exception
        except:
          print("Invalid size")
          maxcolumnlen = 15
      else:
        cur.execute(sql)

        if cur.with_rows:    #check if output contains rows
                             #pretty-print ASCII table
          cols = len(cur.column_names)
          print("╔" + ("═" * maxcolumnlen + "╦") * cols + "\b╗")
                             #column titles
          for y in cur.column_names:
            print(("║{:^{}.{}}").format(str(y), maxcolumnlen, maxcolumnlen), end="")
          print("║")
          print("╠" + ("═" * maxcolumnlen + "╬") * cols + "\b╣")
                             #rows
          for x in cur:
            for y in x:
              print(("║{:^{}.{}}").format(str(y), maxcolumnlen, maxcolumnlen), end="")
            print("║")
          print("╚" + ("═" * maxcolumnlen + "╩") * cols + "\b╝")

        print("Rowcount:", cur.rowcount)
    except Exception as e:
      print(e)

def close():
  db.close()
  return ""

import base64
devs = base64.b64decode("ICAgU09IQU0gUFJFTSBLQVJUSElLJ1MgIA==").decode("ascii")

#driver code if this module is run standalone
if __name__ == "__main__":
  input("If you want to play the game, close this and open 'play_KBC_game.py'")
  sqldirect()
  close()
