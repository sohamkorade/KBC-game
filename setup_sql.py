"""
Run this file to reset/initialize the game database
"""

import mysql.connector  #for SQL connection

print("Connecting to MySQL using default connection string...\n\n<ENTER> = continue, z = change")
if input().lower() == "z":
  print("Enter connection arguments:")
  db = mysql.connector.connect(host=input("host:"), user=input("user:"),
                               password=input("password:"))
else:
  db = mysql.connector.connect(host="localhost", user="root", password="root")
cur = db.cursor()

#execute SQL commands from file 'setup_sql.txt'
print("\nCreating database")
with open("setup_sql.txt") as f:
  for i in f.read().split(";\n"):
    print(".", end="", flush=True)
    try:
      cur.execute(i)
    except:
      pass
db.commit()

#execute SQL commands from files listed in 'LIST_OF_TOPICS.txt'
print("\nAdding questions to database...")
with open("./topics/LIST_OF_TOPICS.txt") as f1:
  topics = f1.read().split("\n")
  for i in topics:
    print("\n\t Adding topic '", i, "'...", sep="")
    with open("./topics/%s.txt" % i) as f2:
      try:
        cur.execute(f2.read())
      except:
        pass

db.commit()
print("\n\nAll done. Now you can open 'play_KBC_game.py' to play the game!")
input()