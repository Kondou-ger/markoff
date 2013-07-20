#!/usr/bin/python3
import sqlite3
from random import choice

class markoff(object):
	def __init__(self, filename):
		self.filename = filename
		self.conn = sqlite3.connect(filename)
		self.cursor = self.conn.cursor()
	
	def __del__(self):
		self.conn.close()
	
	def initdb(self, reset = False):
		if reset:
			self.cursor.execute("DROP TABLE IF EXISTS pairlist")
		self.cursor.execute("CREATE TABLE pairlist (id INTEGER PRIMARY KEY AUTOINCREMENT, first TEXT, second TEXT, isFirst BOOL, isLast BOOL)")
		self.conn.commit()
	
	def addpair(self, first, second, isFirst=False, isLast=False):
		t = [str(first), str(second), str(isFirst), str(isLast)]
		self.cursor.execute("INSERT INTO pairlist (first, second, isFirst, isLast) VALUES (?, ?, ?, ?)", t)
		self.conn.commit()
	
	def add(self, message):
		splitted = message.split()
		if len(splitted) == 2:
			self.addpair(splitted[0], splitted[1], True, True)
		elif len(splitted) > 2:
			for i in range(0, len(splitted)):# for(i=0; i<=len(splitted); i++)
				if i == 0:
					self.addpair(splitted[i], splitted[i+1], True, False)
				elif i == len(splitted)-2:
					self.addpair(splitted[i], splitted[i+1], False, True)
				elif i == len(splitted)-1:
					pass
				else:
					self.addpair(splitted[i], splitted[i+1], False, False)
	
	def getfollow(self, first, isFirst=False):
		t = [str(first), str(isFirst)]
		self.cursor.execute("SELECT second, isLast FROM pairlist WHERE first = ? AND isFirst = ?", t)
		follow = self.cursor.fetchall()
		try:
			return choice(follow)
		except IndexError:
			return []
	
	def create(self, firstword = False, secondword = False):
		message = []
		if firstword:
			message.append(firstword)
			if secondword:
				message.append(secondword)
				isLast = "False"
			else:
				t = [str(firstword)]
				self.cursor.execute("SELECT second, isLast FROM pairlist WHERE first = ?", t)
				second = self.cursor.fetchall()
				chosen = choice(second)
				message.append(chosen[0])
				isLast = chosen[1]
		else:
			t = [str(True)]
			self.cursor.execute("SELECT first, second, isLast FROM pairlist WHERE isFirst = ?", t)
			result = choice(self.cursor.fetchall())
			message.append(result[0])
			message.append(result[1])
			isLast = result[2]
		
		counter = 0 #to prevent infinite loops TODO remove when finished
		while isLast != "True":
			t = [str(message[len(message)-1])]
			self.cursor.execute("SELECT second, isLast FROM pairlist WHERE first = ?", t)
			nextsecond = choice(self.cursor.fetchall())
			message.append(nextsecond[0])
			isLast = nextsecond[1]
			if counter > 3000: # TODO remove when finished
				print("Prevented infinite loop!")
				break
			counter += 1 # TODO remove
		
		return ' '.join(message)
