#!/usr/bin/python3

import markoff

test = markoff.markoff("testing.db")

print("Usage:\n\\? = help\n\\reset = reset db\n\\say word word = say something\n\\quit = quit")
while True:
	line = input(">")
	if line[0] == "\\":
		if line[1:] == "?":
			print("Usage:\n\\? = help\n\\reset = reset db\n\\say word word = say something\n\\quit = quit")
		elif line[1:] == "reset":
			test.initdb(True)
			print("Done.")
		elif line[1:4] == "say":
			splitted = line[1:].split()
			if len(splitted) == 3:
				print(test.create(splitted[1], splitted[2]))
			elif len(splitted) == 2:
				print(test.create(splitted[1]))
			else:
				print(test.create())
		elif line[1:5] == "quit":
			break
	else:
		test.add(line)