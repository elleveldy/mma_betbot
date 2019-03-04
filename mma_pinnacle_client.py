from pinnacleClient import PinnacleClient

import json

username = "ED974228"
password = "#B0tSw4g9"



def pprint(string):
	print(json.dumps(string, indent=4, sort_keys=True))


class MMAClient(PinnacleClient):
	def __init__(self, username, password):
		PinnacleClient.__init__(self, username, password)

		self.sports_id = self.get_sports_id("Mixed Martial Arts")

		self.mma_leagues = self.mma_get_leagues()

		self.odds = None

		self.fixtures = None

	def mma_get_leagues(self):
		return self.get_leagues(self.sports_id)

	def mma_get_league_id(self, league_name):
		for league in self.mma_leagues["leagues"]:
			if league_name == league["name"]:
				return league["id"]

	def mma_get_fixtures(self):
		return self.get_fixtures(self.sports_id)

	def mma_get_event_id(self, league_id, fighter_name):
		if self.fixtures:
			pass
		else:
			self.fixtures = self.mma_get_fixtures()

		for league in self.fixtures["league"]:
			if league["id"] == league_id:
				for event in league["events"]:
					if fighter_name in [ event["home"] , event["away"]]:
						return event["id"]
		return None

	def mma_fighter_home_or_away(self, league_id, fighter_name):
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
		return self.get_odds(self.sports_id, oddsFormat = "Decimal")


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

	def mma_get_line_odds(self, league_id, event_id, line_id, home_or_away):
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
							return event["periods"][0]["moneyline"][home_or_away]
		return None





client = MMAClient(username, password)

print("mma id == {}".format(client.sports_id))
mma_leagues = client.mma_get_leagues()

ufc_id = client.mma_get_league_id("UFC")
bellator_id = client.mma_get_league_id("Bellator")


# odds = client.mma_get_odds()
# pprint(odds)

fixtures = client.mma_get_fixtures()
pprint(fixtures)

jds_event_id = client.mma_get_event_id(ufc_id, "Junior Dos Santos")
jds_home_away = client.mma_fighter_home_or_away(ufc_id, "Junior Dos Santos")
jds_line_id = client.mma_get_line_id(ufc_id, jds_event_id)
jds_odds = client.mma_get_line_odds(ufc_id, jds_event_id, jds_line_id, jds_home_away)


print("eventid for JDS = ", jds_event_id)
print("home or away for JDS = ", jds_home_away)
print("lineId for JDS = ", jds_line_id)
print("line odds for JDS = ", jds_odds)

