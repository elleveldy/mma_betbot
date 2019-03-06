# from mma_pinnacle_client import *
# from bet_mma_tips_events import *
from colored_printing import *
from update_acceptable_odds import update_acceptable_odds
# import execnet

# def call_python_version(Version, Module, Function, ArgumentList):
#     gw      = execnet.makegateway("popen//python=python%s" % Version)
#     channel = gw.remote_exec("""
#         from %s import %s as the_function
#         channel.send(the_function(*channel.receive()))
#     """ % (Module, Function))
#     channel.send(ArgumentList)
#     return channel.receive()

# def Update_odds_file(filename):
# 	call_python_version("2.7", "update_acceptable_odds", "update_acceptable_odds", filename, [])




import subprocess


def update_odds_file(filename):
		
	python3_command = "update_acceptable_odds.py {}".format(filename)  # launch your python2 script using bash

	process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()  # receive output from the python2 script




acceptable_odds_file_name = "acceptable_odds.txt"

Update_odds_file(acceptable_odds_file_name)

acceptable_odds_file = JsonFileHandler(acceptable_odds_file_name)

acceptable_odds = mma_picks_file.read()

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




