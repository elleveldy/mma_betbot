#PYTHON 3

import urllib.request as ulib
import base64
import uuid
import json
from httpRequests import *


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
		print("pinnacle.place_bet with data: {}".format(data))
		return http_post(url, data = data, headers = self.postHeaders)

	def placeBet(self, sportId, eventId, lineId, period, betType, team, stake):
		bet = {"sportId":str(sportId), "eventId":str(eventId), "lineId":str(lineId),
				"period":str( period), "betType":str(betType), "team":str(team)}
		self.place_bet(bet, stake)
		 

