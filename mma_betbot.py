from mma_pinnacle_client import *
from mma_event_file_handler import MMAEventFileHandler
from colored_printing import *

mma_picks_file_name = "test_file_nr_2.json"

mma_picks_file = JsonFileHandler(mma_picks_file_name)

mma_picks = mma_picks_file.read()

printPretty(mma_picks)




