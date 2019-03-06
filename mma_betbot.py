# from mma_pinnacle_client import * from bet_mma_tips_events import * from colored_printing import * from update_acceptable_odds import update_acceptable_odds from json_file_handler import JsonFileHandler

filename = "adequate_odds.txt"

# update_acceptable_odds(filename)

acceptable_odds_file = JsonFileHandler(filename)





printPretty(acceptable_odds)






REQUIRED_ODDS_BENEFIT_MARGIN = 1 # == 100%

def hypothetical_arbitrage(fight):
	odds_0 = fight[0].value()
	odds_1 = fight[1].value()

	arbitrage = 1 / (1 / odds_0  + 1 / odds_1 )

	

# def main():

# 	update_acceptable_odds()
update_acceptable_odds(filename)

# 	sleep()

# 	fight_event_json = get_acceptable_odds_from_file()
acceptable_odds = acceptable_odds_file.read()
for event in acceptable_odds:

	for fight in event["fights"]:

		for fighter in fight:

# 				bet = find_bet(event, fighter):

# 				if bet:

# 					if estimated_roi(fighter, bet) >= required_roi:

# 						place_bet(bet)
# 						placed_bets.write(bet)



