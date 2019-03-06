from mma_pinnacle_client import * 
from bet_mma_tips_events import * 
from colored_printing import * 
from update_acceptable_odds import update_acceptable_odds 
from json_file_handler import * 

filename = "odds_file.txt"

# update_acceptable_odds(filename)

acceptable_odds_file = JsonFileHandler(filename)


REQUIRED_ODDS_BENEFIT_MARGIN = 1.00 # == 100%



username = file_get_username("account_info.txt")
password = file_get_password("account_info.txt")
pinnacle = MMAPinnacleClient(username, password)


acceptable_odds = acceptable_odds_file.read()

pinnacle_odds = pinnacle.mma_get_odds()

printPretty(pinnacle_odds)

def is_bet_worth_it(bet, fighter):
	#TODO: make sure we don't add fighters with zero odds...

	if fighter["odds"] == None or fighter["odds"] < 1:
		return False
	try:
		odds_margin = float(float(bet["odds"]) / float(fighter["odds"]))
		if  odds_margin >= REQUIRED_ODDS_BENEFIT_MARGIN:
			return True
		else:
			return False
	except ZeroDivisionError:
		printError("is_bet_worth_it ZeroDivisionError with bet {}\nfighter {}".format(bet, fighter))
		return False


placed_bets = JsonFileHandler("placed_bets.txt")

betting_log = JsonFileHandler("betting_log.txt")


def hypothetical_arbitrage(fight):
	printBlue(fight)
	if not (fight[0] and fight[1]):
		return False
	odds_0 = fight[0]["odds"]
	odds_1 = fight[1]["odds"]
	if (odds_0 < 1.0) or (odds_1 < 1.0):
		return False
	arbitrage = 1 / (1 / odds_0  + 1 / odds_1 )
	if arbitrage > 1.0:
		return True
	else:
		True

for event in acceptable_odds:

	for fight in event["fights"]:

		for fighter in fight:
			if fighter:
				bet = pinnacle.mma_get_bet(event["organization"], fighter["name"])
				if(bet):
					if(is_bet_worth_it(bet, fighter) and hypothetical_arbitrage(fight)):
						printGreen("Bet worth: {}".format(fighter))
						if not placed_bets.has_element(bet):
							printGreen("Not already in placed_bets")
							placed_bets.write(bet)
							stake = 15
							logged_bet = bet
							logged_bet["stake"] = stake
							betting_log.write(logged_bet)
							pinnacle.mma_place_bet(bet, stake)
							printGreen("**********************************************\nPlaced bet: {}\n***********************************************".format(bet))
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



