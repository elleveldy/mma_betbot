from mma_pinnacle_client import *
from mma_event_file_handler import MMAEventFileHandler
from colored_printing import *

mma_picks_file_name = "test_file_nr_2.json"

mma_picks_file = JsonFileHandler(mma_picks_file_name)

mma_picks = mma_picks_file.read()

printPretty(mma_picks)






# required_roi = 0.1 # == 10%

# def estimated_roi(fighter, bet);
# 	return float(float(bet["odds"]) / float(fighter["odds"]))

# def hypothetical_arbitrage(fight):
# 	odds_0 = fight[0].value()
# 	odds_1 = fight[1].value()

# 	arbitrage = 1 / (1 / odds_0  + 1 / odds_1 )

	

# def main():

# 	update_acceptable_odds()		#This will need to be called as python 2


# 	sleep()

# 	fight_event_json = get_acceptable_odds_from_file()

# 	for event in fight_event_json:

# 		for fight in event:

# 			for fighter in fight:

# 				bet = find_bet(event, fighter):

# 				if bet:

# 					if estimated_roi(fighter, bet) >= required_roi:

# 						place_bet(bet)
# 						placed_bets.write(bet)




