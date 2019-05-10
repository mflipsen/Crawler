from setup import base, case
from general import create_project_dir, dir_case, dir_Crawler, create_setup
from crawler import crawl_case
from scraper import scrape_case
from reader import read_information

# =============================================================================
# Main function to run the program
# =============================================================================


def run():
    # create a folder to store all case related files and set dir to the folder
    create_project_dir(case)
    dir_case(base, case)
    # execute main crawl functions
    crawl_case()
    # execute main scrape functions
    scrape_case()
    # create setup file
    create_setup()


# =============================================================================
# Run the code below to start the program
# =============================================================================

run()

# =============================================================================
# Optional: create separate .txt-files for each keyword
# =============================================================================

read_information()

# =============================================================================
# Optional: go back to Crawler directory
# =============================================================================

dir_Crawler(base)
