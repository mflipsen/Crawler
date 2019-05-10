from pathlib import Path
import time


# Directory settings
case = "TechSoup.org"
base = Path.cwd()

# Date and time of running program
datetime = time.strftime("%x") + ' ' + time.strftime("%H:%M")

# Googler settings
query = case
maxresults = 10

# Crawler settings
maxthreads = 8
