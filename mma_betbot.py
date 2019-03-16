from mma_pinnacle_client import * 
from bet_mma_tips_events import * 
from colored_printing import * 
from update_acceptable_odds import update_acceptable_odds 
from json_file_handler import * 
import time
from bet_evaluation import *






# def main():



print("Starting cycle...")

username = file_get_username("account_info.txt")
password = file_get_password("account_info.txt")
pinnacle = MMAPinnacleClient(username, password)
pinnacle_odds = pinnacle.mma_get_odds()	
pinnacle.mma_print_economic_status()


acceptable_odds_filename = "odds_file.txt"
acceptable_odds_file = JsonFileHandler(acceptable_odds_filename)
placed_bets = BetLogFile("placed_bets.txt")


while True:

	update_acceptable_odds(acceptable_odds_filename)

	stake = pinnacle.one_unit

	acceptable_odds = acceptable_odds_file.read()

	for event in acceptable_odds:
		for fight in event["fights"]:

			for fighter in fight:

				if fighter:
					bet = pinnacle.mma_get_bet(event["organization"], fighter["name"])

					if(bet):

						if(is_bet_worth_it(bet, fighter)):

							already_placed_bets = placed_bets.find(bet)

							if not already_placed_bets: 

								print("\t\tBetlog: ***************************************************************************************************")
								for bets in placed_bets.read():
									print("\t\t{}".format(bets))
								print("\t\tBetlog: ***************************************************************************************************")

								bet["stake"] = stake
								placed_bets.write(bet)
								# pinnacle.mma_place_bet(bet, stake)

								printGreen("\t\tPlaced bet: {}".format(bet))

							else:

								if is_significantly_improved_odds(already_placed_bets, bet): 

									printGreen("\t\t\t\tDetected already placed bet with significantly improved odds!")
									printGreen("\t\t\t\tOld bet list: {}".format(already_placed_bets))
									printGreen("\t\t\t\tNew bet: {}".format(bet))

									bet["stake"] = stake * 0.6
									# pinnacle.mma_place_bet(bet, stake)
									printGreen("\t\tPlaced bet: {}".format(bet))
								else:
									pass
						else:
							pass
					else:
						pass
				else:
					pass		
	printBlue("***************************************************************************************************************")	
	printBlue("Cycle complete, sleeping for 600 sec (10 min)")
	printBlue("***************************************************************************************************************")	
	time.sleep(600)
