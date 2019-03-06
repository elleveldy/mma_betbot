from bet_mma_tips_events import * BetMMATipsEvent
from json_file_handler import JsonFileHandler

def update_acceptable_odds(file_name):

	for event_url in get_free_betting_tip_urls():

		event = BetMMATipsEvent(event_url)

		print(event.eventDictionary)

		file = JsonFileHandler(file_name)
		file.write(event.eventDictionary)


def get_free_betting_tip_urls():
	lookup_page_url = "https://www.betmma.tips/mma_betting_tips.php"

	page = requests.get(lookup_page_url)

	soup = BeautifulSoup(page.content, 'html.parser')

	lookup_table = soup.find('td', {'bgcolor': '#F7F7F7'}).find("table").find_all("tr")

	event_list = []

	for element in lookup_table[1:len(lookup_table)]:

	 	td_tag_list = element.find_all("td")
		event_dict = {}

		event_dict["dict"] = td_tag_list[0].get_text()
		event_dict["eventName"] = td_tag_list[2].find("a").get("title").split(" for ")[1]
		event_dict["url"] = str("https://www.betmma.tips/") + str(td_tag_list[2].find("a").get("href"))

		event_list.append(event_dict)

	event_url_list = []
	for event in event_list:
		event_url_list.append(event["url"])

	return event_url_list



update_acceptable_odds("events4.txt")