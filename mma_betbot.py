from mma_pinnacle_client import * 
from bet_mma_tips_events import * 
from colored_printing import * 
from update_acceptable_odds import update_acceptable_odds 
from json_file_handler import * 
import time
from bet_evaluation import *

#Get minimum bet amount from pinnacle?
MINIMUM_BET_AMOUNT = 12



# def main():



print("Starting cycle...")

username = file_get_username("account_info.txt")
password = file_get_password("account_info.txt")
pinnacle = MMAPinnacleClient(username, password)
pinnacle_odds = pinnacle.mma_get_odds()	
pinnacle.mma_print_economic_status()


placed_bets = BetLogFile("placed_bets.txt")


minute_count = 0
hour_count = 0


while True:
	
	acceptable_odds = update_acceptable_odds()

	pinnacle.mma_update_economic_status()

	stake = pinnacle.one_unit

	for event in acceptable_odds:
		for fight in event["fights"]:

			for fighter in fight:

				if fighter:

					bet = pinnacle.mma_get_bet(event["organization"], fighter["name"])

					if(bet):

						if(is_bet_worth_it(bet, fighter) and is_hypothetical_arbitrage(fight)):

							already_placed_bets = placed_bets.find(bet)

							if not already_placed_bets: 

								stake = max(pinnacle.one_unit * get_stake_ratio(bet, fighter), MINIMUM_BET_AMOUNT)
								bet["stake"] = stake

								response = pinnacle.mma_place_bet(bet, stake)

								if response["status"] != "PROCESSED_WITH_ERROR":
									placed_bets.write(bet)
								else:
									printError("Bet placement processed with error...\n{}".format(response))
								
								printYellow("Acceptable odds for fighter: \n{}\nPlaced bet: {}".format(fighter, bet))
								pinnacle.mma_print_economic_status()


							else:

								if is_significantly_improved_odds(already_placed_bets, bet): 

									printGreen("Detected already placed bet with significantly improved odds!\nOld bet list: {}\nNew bet: {}".format(already_placed_bets, bet))

									stake = placed_bets.get_lowest_stake(bet) * 0.8
									if stake > pinnacle.one_unit * 0.8:
										printError("STAKE {}, higher than expected, abort placing bet".format(stake))
										break
									bet["stake"] = stake
									response = pinnacle.mma_place_bet(bet, stake)

									if response["status"] != "PROCESSED_WITH_ERROR":
										placed_bets.write(bet)
										printGreen("Placed bet: {}".format(bet))
										pinnacle.mma_print_economic_status()
									else:
										printError("Bet placement processed with error...\n{}".format(response))


	time.sleep(300)
	minute_count += 5
	if(not minute_count % 60):
		minute_count = 0
		hour_count += 1
	print("{} hours and {} minutes have passed".format(hour_count, minute_count))
