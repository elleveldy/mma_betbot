from pinnacle_client import PinnacleClient
from colored_printing import *
# from json_file_handler import JsonFileHandler, file_get_password, file_get_username


#TODO: Edit the get functions such that they utilize the since paramter.

class MMAPinnacleClient(PinnacleClient):
	def __init__(self, username, password):
		PinnacleClient.__init__(self, username, password)

		self.sports_id = self.get_sports_id("Mixed Martial Arts")

		self.mma_leagues = self.mma_get_leagues()

		self.odds = None

		self.fixtures = None
		
		#Economic parameters ##############################################################
		self.balance = self.get_balance()
		self.available_balance = self.balance["availableBalance"]	
		self.outstanding_transactions = self.balance["outstandingTransactions"]
		self.total_balance = self.available_balance + self.outstanding_transactions	
		self.unit_fraction = 0.05
		self.one_unit = round(self.total_balance * self.unit_fraction, 2)
		###################################################################################

	def mma_update_economic_status(self):
		self.balance = self.get_balance()
		self.available_balance = self.balance["availableBalance"]
		self.outstanding_transactions = self.balance["outstandingTransactions"]
		self.total_balance = self.available_balance + self.outstanding_transactions 
		self.one_unit = round(self.total_balance * self.unit_fraction, 2)

	def mma_print_economic_status(self):
		self.mma_update_economic_status()
		printBlue("******************************************************************")
		printBlue("MMAPinnacleClient economic status:\nBalance = {}".format(self.balance))

		printBlue("self.available_balance = {}".format(self.available_balance))
		printBlue("self.outstanding_transactions = {}".format(self.outstanding_transactions))
		printBlue("self.total_balance = {}".format(self.total_balance))
		printBlue("self.one_unit = {}".format(self.one_unit))

		printBlue("******************************************************************")


	def mma_get_leagues(self):
		return self.get_leagues(self.sports_id)

	def mma_get_league_id(self, league_name):
		for league in self.mma_leagues["leagues"]:
			if league_name == league["name"]:
				return league["id"]

	def mma_get_fixtures(self):
		return self.get_fixtures(self.sports_id)

	def mma_get_event_id(self, league_id, fighter_name):
		# FIX FIGHTER NAME PARSING
		if self.fixtures:
			pass
		else:
			self.fixtures = self.mma_get_fixtures()

		for league in self.fixtures["league"]:
			if league["id"] == league_id:
				for event in league["events"]:
					if (fighter_name in  event["home"]) or (fighter_name in event["away"]):
						return event["id"]
		return None

	def mma_get_fighter_team(self, league_id, fighter_name):
	#FIX FIGHTER NAME PARSING
		if self.fixtures:
			pass
		else:
			self.fixtures = self.mma_get_fixtures()

		for league in self.fixtures["league"]:
			if league["id"] == league_id:
				for event in league["events"]:
					if fighter_name in event["home"]:
						return "home"
					if fighter_name in event["away"]:
						return "away"

#############  UTILIZE ODDS INSTEAD OF FIXTURES BELOW ####################################################################

	def mma_get_odds(self):
		odds = self.get_odds(self.sports_id, oddsFormat = "Decimal")
		# printPretty(odds)
		return odds

	def mma_update_odds(self):
		since = self.odds["since"]
		odds_since = self.get_odds(self.sports_id, oddsFormat = "Decimal", since = since)
		printPretty(odds_since)
		return odds_since

	def mma_get_line_id(self, league_id, event_id):
		"""
				For now only accepts moneyline bets,
				if we want other kinds of bets, we need to add
				check the periods:[] list for bets of others types
				and return their line number
		"""
		if self.odds:
			pass
		else:
			self.odds = self.mma_get_odds()

		for event in self.odds["leagues"][0]["events"]:
			if event_id == event["id"] and "moneyline" in event["periods"][0]:
				return event["periods"][0]["lineId"]
		return None

	def mma_get_line_odds(self, league_id, event_id, line_id, team):
		"""
				For now only accepts moneyline bets,
				if we want other kinds of bets, we need to add
				check the periods:[] list for bets of others types
				and return their line number
		"""
		if self.odds:
			pass
		else:
			self.odds = self.mma_get_odds()

		for league in self.odds["leagues"]:
			if league["id"] == league_id:
				for event in league["events"]:
					if event_id == event["id"]:
						if line_id == event["periods"][0]["lineId"]:
							return event["periods"][0]["moneyline"][team]
		return None



##########################################################################################################################

	



##########################################################################################################################

	def mma_get_bet(self, league_name, fighter_name):

		"""
			This function currently only supports moneyline bets at "period": 0
		"""
		league_id = self.mma_get_league_id(league_name)
		fighter_event_id = self.mma_get_event_id(league_id, fighter_name)
		fighter_team = self.mma_get_fighter_team(league_id, fighter_name)
		fighter_line_id = self.mma_get_line_id(league_id, fighter_event_id)
		fighter_odds = self.mma_get_line_odds(league_id, fighter_event_id, fighter_line_id, fighter_team)
		mma_bet = {
			"leagueName": league_name,
			"fighterName": fighter_name,
			"eventId": fighter_event_id,
			"lineId": fighter_line_id,
			"team": fighter_team,
			"odds": fighter_odds
		}
		if (league_id and fighter_event_id and fighter_team and fighter_line_id and fighter_odds):
			return mma_bet
		else:
			# print("mma_get_bet: bet not found for league: {}, fighter{}, returning None".format(league_name, fighter_name))
			pass


	def mma_place_bet(self, mma_bet, stake):
		"""
			This function currently only supports moneyline bets at "period": 0

			mma_bet_format = {
				"eventId": "123123123",
				"lineId": "123123123",
				"team":	"home"
			}

		"""

		if mma_bet["team"] == "home":
			team = "Team1"
		if mma_bet["team"] == "away":
			team = "Team2"

		pinnacle_client_bet = {
			"eventId":str(int(mma_bet['eventId'])),            
			"lineId":str(int(mma_bet['lineId'])),
			"team": team,
			# "team":"TEAM1",
			"stake": str(float(stake)),

			"sportId": str(self.sports_id),
			"period": "0",
			"betType": "moneyline",
		}
		http_post = self.place_bet(pinnacle_client_bet, stake)
		return http_post


