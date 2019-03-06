

required_roi = 0.1 # == 10%

def estimated_roi(fighter, bet);
	return float(float(bet["odds"]) / float(fighter["odds"]))

def hypothetical_arbitrage(fight):
	odds_0 = fight[0].value()
	odds_1 = fight[1].value()

	arbitrage = 1 / (1 / odds_0  + 1 / odds_1 )

	

def main():

	update_acceptable_odds()		#This will need to be called as python 2


	sleep()

	fight_event_json = get_acceptable_odds_from_file()

	for event in fight_event_json:

		for fight in event:

			for fighter in fight:

				bet = find_bet(event, fighter):

				if bet:

					if estimated_roi(fighter, bet) >= required_roi:

						place_bet(bet)
						placed_bets.write(bet)




