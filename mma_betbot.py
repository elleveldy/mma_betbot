from mma_pinnacle_client import * 
from bet_mma_tips_events import * 
from colored_printing import * 
from update_acceptable_odds import update_acceptable_odds 
from json_file_handler import * 
import time
from bet_evaluation import *






# def main():

while True:


	print("Starting cycle...")

	username = file_get_username("account_info.txt")
	password = file_get_password("account_info.txt")
	pinnacle = MMAPinnacleClient(username, password)
	pinnacle_odds = pinnacle.mma_get_odds()	
	pinnacle.mma_print_economic_status()


	acceptable_odds_filename = "odds_file.txt"
	acceptable_odds_file = JsonFileHandler(acceptable_odds_filename)
	placed_bets = BetLogFile("placed_bets.txt")


	# while True:

	update_acceptable_odds(acceptable_odds_filename)
	stake = pinnacle.one_unit
	acceptable_odds = acceptable_odds_file.read()

	for event in acceptable_odds:
		for fight in event["fights"]:

			for fighter in fight:

				if fighter:
					bet = pinnacle.mma_get_bet(event["organization"], fighter["name"])

					if(bet):

						if(is_bet_worth_it(bet, fighter) and is_hypothetical_arbitrage(fight)):
							printGreen("Bet worth: {}".format(fighter))


							already_placed_bets = placed_bets.find(bet)

							if not already_placed_bets: 
								printBlue("Not already in placed_bets")


								bet["stake"] = stake
								placed_bets.write(bet)
								# pinnacle.mma_place_bet(bet, stake)

								printGreen("**********************************************\nPlaced bet: {}\n***********************************************".format(bet))
							elif is_significantly_improved_odds(already_placed_bets, bet): 

								printBlue("Detected already placed bet with significantly improved odds!")
								printBlue("Old bet list: {}".format(already_placed_bets))
								printBlue("New bet: {}".format(bet))

								bet["stake"] = stake * 0.6
							else:
								printError("Bet, {}\nalready in placed_bets.txt".format(bet))
						else:
							pass
					else:
						# printYellow("no bet")	
						pass
				else:
					#TODO: fix this v
					# printYellow("Nonefighter in fight (usually means no-one bet on this fighter... Maybe don't add them to dictionary then?)")
					pass		
	print("Cycle complete, sleeping for 60 sec")
	time.sleep(3)

# main()