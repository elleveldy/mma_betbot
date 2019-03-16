from colored_printing import *


REQUIRED_ODDS_BENEFIT_MARGIN = 1.00 # == 100%



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

def is_hypothetical_arbitrage(fight):
	# printBlue(fight)
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

def is_significantly_improved_odds(already_placed_bets, new_bet):
	"""
		checks if a bet that we've already placed, is worth placing again, if odds have improved significantly
		TODO: Compare to betmma_odds to determine that acceptable odds haven't dropped significantly
	"""
	significant_improvement_ratio = 1.05			#sort of arbitrary number
	try:
		for old_bet in already_placed_bets:
			ratio = float(new_bet["odds"] / float(old_bet["odds"]))
			if not(ratio) >= float(significant_improvement_ratio):
				return False
		printGreen("Significant improvement detected for {}".format(new_bet))
		return True
	except ZeroDivisionError:
		printError("is_significantly_improved_odds ZeroDivisionError with placed_bet= {},\n new_bet = {}\nRatio = {}".format(palced_bet, new_bet, ratio))
		return False
