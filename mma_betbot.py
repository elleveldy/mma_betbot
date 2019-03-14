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
							# printYellow("**************************************************")
							# printYellow("Fighter worth: {}, with bet:\n{}".format(fighter, bet))
							# printYellow("**************************************************")

							# print("\t**************************************************")
							# print("\tSince we found worthy bet, lets check what's up")
							# print("\tfight = {}, \n\tfighter = {},\n\tbet = {}".format(fight, fighter, bet))	
							# print("\t**************************************************")

							already_placed_bets = placed_bets.find(bet)

							if not already_placed_bets: 

								printYellow("\t\tBet: {},\n\t\talready placed_bets: {}".format(bet, already_placed_bets))
								print("\t\tBetlog: ***************************************************************************************************")
								for bets in placed_bets.read():
									print("\t\t{}".format(bets))
								print("\t\tBetlog: ***************************************************************************************************")

								bet["stake"] = stake
								placed_bets.write(bet)
								pinnacle.mma_place_bet(bet, stake)

								printGreen("\t\tPlaced bet: {}".format(bet))

							else:
								# printYellow("\t\t\t\tBet, {}\n\t\t\t\talready in placed_bets.txt".format(bet))

								if is_significantly_improved_odds(already_placed_bets, bet): 

									# printGreen("\t\t\t\tDetected already placed bet with significantly improved odds!")
									# printGreen("\t\t\t\tOld bet list: {}".format(already_placed_bets))
									# printGreen("\t\t\t\tNew bet: {}".format(bet))

									bet["stake"] = stake * 0.6
									pinnacle.mma_place_bet(bet, stake)
									printGreen("\t\tPlaced bet: {}".format(bet))
								else:
									# printError("\t\t\t\tNo significantly improved odds")
									pass
						else:
							# printError("Bet not worth it: {}".format(bet))
							pass
					else:
						# printYellow("no bet")	
						pass
				else:
					#TODO: fix this v
					# printYellow("Nonefighter in fight (usually means no-one bet on this fighter... Maybe don't add them to dictionary then?)")
					pass		
	printBlue("***************************************************************************************************************")	
	printBlue("\n\n\n\n\n\n\nCycle complete, sleeping for 600 sec (10 min)\n\n\n\n\n\n\n\n")
	printBlue("***************************************************************************************************************")	
	time.sleep(600)
