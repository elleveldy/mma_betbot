#PYTHON 3

import urllib.request as ulib
import base64
import uuid
import json
from httpRequests import *
import pprint

MLB_league_id = 246

class PinnacleClient():
	def __init__(self, username, password):
		b64str = base64.b64encode("{}:{}".format(username,password).encode('utf-8'))

		self.username = username
		self.password = password
		self.getHeaders = {
			'Content-length' : '0',
			'Content-type' : 'application/json',
			'Authorization' : "Basic " + b64str.decode('utf-8')
		}
		self.postHeaders = {
			'Content-length' : '1',
			'Content-type' : 'application/json',
			'Authorization' : "Basic " + b64str.decode('utf-8')
		}
		self.sport_json = self.get_sports()

	def get_bets(self, betlist = 0, betids = 0, fromDate = 0, toDate = 0):
		url = "https://api.pinnacle.com/v1/bets=" 
		if(betids): 
			url = url + "&betids=" + str(betids)
			return http_get(url, headers=self.getHeaders)
		if(betlist): url = url + "betlist=" + str(betlist)
		if(fromDate): url = url + "&fromDate=" + str(fromDate)    
		if(toDate): url = url + "&toDate=" + str(toDate)
		print("*********\nUrl:", url)
		return http_get(url, headers=self.getHeaders)

	def get_balance(self):
		url = "https://api.pinnacle.com/v1/client/balance"
		return http_get(url, headers=self.getHeaders)

	def get_sports(self):
		url = "https://api.pinnacle.com/v2/sports"
		self.sports = http_get(url, headers=self.getHeaders)
		return self.sports

	def get_sports_id(self, sport_name):
		for sport in self.sport_json["sports"]:
			if sport["name"] == sport_name:
				return sport["id"]

	def get_leagues(self, sportid):
		url = 'https://api.pinnacle.com/v2/leagues?sportid=' + str(sportid)
		return http_get(url, headers=self.getHeaders)

	def get_fixtures(self, sportId, leagueIds = 0, since = 0, isLive = 0, oddsFormat = 0, eventIds = 0):
		url = 'https://api.pinnacle.com/v1/fixtures?sportId=' + str(sportId)
		if(since): url = url + "&since=" + str(since)
		if(isLive): url = url + "&isLive=" + str(isLive)    
		if(eventIds): url = url + "&eventIds=" + str(eventIds)
		if(leagueIds): url = url + "&leagueIds=" + str(leagueIds)   
		return http_get(url, headers=self.getHeaders)

	def get_odds(self, sportId, leagueIds = 0, since = 0, isLive = 0, oddsFormat = 0, eventIds = 0):
		url = 'https://api.pinnacle.com/v1/odds?sportid=' + str(sportId)
		if(since): url = url + "&since=" + str(since)
		if(isLive): url = url + "&isLive=" + str(isLive)    
		if(oddsFormat): url = url + "&oddsFormat=" + str(oddsFormat)    
		if(eventIds): url = url + "&eventIds=" + str(eventIds)
		if(leagueIds): url = url + "&leagueIds=" + str(leagueIds)
		print("get_odds\n leagueIds: ", url)

		return http_get(url, headers=self.getHeaders)

	def place_bet(self, bet, stake):
		#Bet is a dictionary with format as "data"-variable bellow
		url = "https://api.pinnacle.com/v1/bets/place"
		data = {
				"uniqueRequestId":uuid.uuid4().hex,
				"acceptBetterLine": str(True),
				"stake": str(float(stake)),
				"winRiskStake":"RISK",
				"sportId":str(int(bet['sportId'])),
				"eventId":str(int(bet['eventId'])),            
				"lineId":str(int(bet['lineId'])),
				"periodNumber":str(int(bet['period'])), #0,1 or 2
				"betType":str(bet['betType']), #might not be moneyline
				"team":bet['team'],	#Team1 or Team2
				"oddsFormat":"DECIMAL"
		}
		return http_post(url, data = data, headers = self.postHeaders)

	def placeBet(self, sportId, eventId, lineId, period, betType, team, stake):
		bet = {"sportId":str(sportId), "eventId":str(eventId), "lineId":str(lineId),
				"period":str( period), "betType":str(betType), "team":str(team)}
		self.place_bet(bet, stake)
		 
	def getMLBOddsWithTeamNames(self):
		MLB_events = client.get_odds(3, leagueIds = MLB_league_id, oddsFormat = "DECIMAL")
		events = MLB_events["leagues"][0]["events"]

		MLB_fixtures = client.get_fixtures(3, leagueIds = MLB_league_id)
		fixtures = MLB_fixtures["league"][0]["events"]


		for event in events:
			for fix in fixtures:
				if event["id"] == fix["id"]:
					event["homeTeam"] = fix["home"]
					event["Team2"] = fix["home"]
					event["awayTeam"] = fix["away"]
					event["Team1"] = fix["away"]
		return events


# username = "ED974228"
# password = "#B0tSw4g9"

# client = PinnacleClient(username, password)


# print("client.getbalance:\n", client.get_balance())

# events = client.getMLBOddsWithTeamNames()
# print(events)

# bet = {
#       "uniqueRequestId":uuid.uuid1().hex,
#       "acceptBetterLine": "True",
#       "oddsFormat":"DECIMAL",
#       "stake": str(13),
#       "winRiskStake":"RISK",
#       "sportId":str(3),
#       "eventId":str(738341297),  
#       "period":"0",     
#       "betType":"MONEYLINE",
#       "team": 'Team1',
#       "lineId":str(402941863)
# }
# client.place_bet(bet, 0.01)

# client.placeBet(3,738341297,402941863,0,"MONEYLINE","Team2",0.1)

# pp = pprint.PrettyPrinter(indent = 1)


# pp.pprint(events)

# print(client.get_balance())