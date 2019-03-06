import json
from commentFinder import *


"""
format:

json = [
	
	{
	date: 12-12-12
	"eventName": UFC 235,
	"event_id" : 12312314134,
	"bet_type" : "moneyline",
	"line_id" : 123123123123,
	"fighter_name": dos,
	"team" : home,
	"odds" : 3.14,
	}



]
"""


class jsonFileHandler():
	def __init__(self, filename):
		self.filename = filename
		try:
			file = open(str(self.filename),"r")
			file.close()
		except FileNotFoundError:
			file = open(str(self.filename), "w")
			betLog = {str(updateMLBDailyDate()): {}}
			json.dumps(betLog, file)
			file.close()

	def read(self):
		file = open(str(self.filename),"r")
		try:
			betLog = json.load(file)
			file.close()
		except FileNotFoundError:
			file = open(str(self.filename), "w")
			betLog = {str(updateMLBDailyDate()): {}}
			json.dumps(betLog, file)
			file.close()
		except ValueError:
			#Needs to return empty date dict if empty, how to pick the correct date?
			#(Correct date not neccessarily current local date)
			betLog = {str(updateMLBDailyDate()): {}}
			file.close()
		return betLog


	def writeBets(self, betDict): 
		print ("Writing bets to: ", str(self.filename))

		user = betDict['user']
		date = betDict['date']
		bets = betDict['bets']

		betLog = self.read()

		try:
			betLog[date][user] = bets
		except KeyError:
			betLog[date] = {}
			betLog[date][user] = bets
			
		with open(str(self.filename), 'w') as file:
			json.dump(betLog, file)
		file.close()

	def writeBet(self, date, user, bet):
		print("*************\nWriting", bet, " to " , str(self.filename))
		betLog = self.read()
		if(not date in betLog):
			print("NO date:", date)
			betLog[date] = {'user': [bet]}
			with open(str(self.filename), 'w') as file:
				json.dump(betLog, file)
			file.close()
			return
		if(not user in betLog[date]):
			print("NO user:", user)
			betLog[date][user] = [bet]
			with open(str(self.filename), 'w') as file:
				json.dump(betLog, file)
			file.close()
			return
		betLog[date][user].append(bet)
		with open(str(self.filename), 'w') as file:
			json.dump(betLog, file)
		file.close()
		return

	def hasBet(self, date, user, bet):
		print(self.filename,".hasBet()")
		betLog = self.read()
		print("\n\n**************\nbetLog:\n", betLog)

		if(not str(date) in betLog):	return False
		if(not str(user) in betLog[date]):	return False
		if bet in betLog[date][user]:
			print(bet, "====", betLog[date][user])
			return True
		else:
			return False

pickFile = jsonFileHandler("picks.json")
placedFile = jsonFileHandler("placedBets.json")

# placedFile.writeBet("27/6/17", "ratbehr", {'team': 'white sox', 'odds': 2.27, 'units': 0.7874015748031495})
# pickFile.writeBet("27/6/17", "ratbehr", {'team': 'white sox', 'odds': 2.27, 'units': 0.7874015748031495})
