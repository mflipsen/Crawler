import os
import re
import csv
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from setup import case, base
from general import pickle_file, create_project_dir
from general import dir_case, dir_Crawler, dir_scrapelist, dir_crawled
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from translate import Translator

# variables for scraping
directory_list = []
scrape_list = []
folder = case + '_scraper'
html = []
text_list = []

# variables for text processing
cleaned = []
cleaned1 = []
cleaned2 = []
sentences = []
keys = []

# variables for information collection
case_info = {}

# =============================================================================
# Main scraper function
# =============================================================================


def scrape_case():
    create_tagslist()
    create_scrapelist()
    scrape_scrapelist()
    process_text()
    collect_info()

# =============================================================================
# Supporting scraper functions
# =============================================================================


def create_tagslist():
    # go back to base directory to access html _text_elements.csv
    dir_Crawler(base)
    with open('html_text_elements.csv', newline='') as f:
        for row in csv.reader(f):
            html.append(row)


def create_scrapelist():
    scrape_links = []
    global scrape_list
    # go back to case crawled directory to store scrape results in crawl folder
    dir_crawled(base, case)

    # list the directories for each project folder
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for name in dirs:
            directory_list.append(os.path.join(root, name))

    # collect urls from all crawled.txt files and append to scrapelist
    for root, name in enumerate(directory_list):
        if (case + '_crawler') in name:
            file = Path.cwd().joinpath(name).joinpath("crawled.txt")
            with open(file) as f:
                for url in f:
                    scrape_links.append(url)

    # clear directory list, remove duplicates and go back to case folder
    directory_list.clear()
    scrape_list = list(dict.fromkeys(scrape_links))
    dir_case(base, case)

    # create scraper folder to save scrapelist to, then go back to temp dir
    create_project_dir(folder)
    dir_scrapelist(base, case)
    pickle_file("scrape_list.txt", scrape_list)
    dir_case(base, case)


def get_pars(soup):
    global text_list

    # retrieve text for all 'p' tags
    pars = [''.join(s.findAll(text=True)) for s in soup.findAll('p')]

    # if there are no 'p' tags, retrieve other text tags and append to list
    if not pars:
        for tag in enumerate(html):
            for i in range(len(soup.find_all(tag))):
                text_list.append(soup.find_all(tag)[i].get_text())

    # if there are 'p' tags, append this text to list
    else:
        text_list += pars


def scrape_scrapelist():
    global scrape_list
    for index, url in enumerate(scrape_list):

        # create a soup for each url in scrape_list
        try:
            r = requests.get(url, timeout=1)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, "html.parser")
            time.sleep(5)

        # in case of errors continue with next url in scrape_list
        # (open source code)
        except requests.exceptions.RequestException as err:
            print("RequestException: ", err)
            continue
        except requests.exceptions.HTTPError as errh:
            print("Http Error: ", errh)
            continue
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting: ", errc)
            continue
        except requests.exceptions.Timeout as errt:
            print("Timeout Error: ", errt)
            continue

        # collect all text data in 'text_list', returns text_list
        get_pars(soup)


# =============================================================================
# Supporting text processing functions
# =============================================================================


# Main processor function
def process_text():
    # prepare text data for processing using various cleaning functions
    prep_text()

    # create list of keywords to look for in data
    create_keyslist()


# Removes all non words and create sentences with all lower cases (open source)
def clean_text():
    global cleaned
    global text_list
    for t in text_list:
        clean = [s.lower() for s in sent_tokenize(t)]
        cleaned += clean
    return cleaned


# Removes duplicates
def remove_dups(cleaned):
    global cleaned1
    cleaned1 = list(dict.fromkeys(cleaned))
    return cleaned1


# Remove all non words from the sentence
def clean_sentences(cleaned1):
    global cleaned2
    for sent in cleaned1:
        cleaned2.append(word_tokenize(sent))
    return cleaned2


# Make all sentences a string
def string_sentences(cleaned2):
    global sentences
    for sent in cleaned2:
        sentence = (' '.join(sent))
        sentences.append(sentence)
    print(sentences)
    return sentences


# Main control function for cleaning
def prep_text():
    clean_text()
    remove_dups(cleaned)
    clean_sentences(cleaned1)
    string_sentences(cleaned2)


# Main keys function
def create_keyslist():
    create_keys()
    extend_keyslist()


# Finds all possible synonyms for the keyswords in 'keys'
def find_synonyms_all():
    global keys
    syns = []
    added = 0
    for keyword in keys:
        for syn in wordnet.synsets(keyword):   # (open source code)
            for lm in syn.lemmas():
                syns.append(lm.name())
    for syn in syns:
        keys.append(syn)
        added += 1
    print("Added " + str(added) + " synonyms to list of keywords 'keys'")


# Finds synonyms for the first synset belonging to the keywords in 'keys'
def find_lemmas():
    global keys
    lems = []
    added = 0
    for keyword in keys:
        syn = wordnet.synsets(keyword)
        try:
            # (open source code)
            for l in [lemma.name() for lemma in syn[0].lemmas()]:
                lems.append(l)
        except IndexError:
            print("No synonyms available")
            continue
    for lem in lems:
        keys.append(lem)
        added += 1
    print("Added " + str(added) + " synonyms to list of keywords 'keys'")
    return keys


# Finds Dutch translations for the keywords given by the user
def find_translations():
    global keys
    dutch = Translator(to_lang="Dutch")
    tls = []
    added = 0
    for keyword in keys:
        t = dutch.translate(keyword)
        tls.append(t)
        time.sleep(0.1)
    for tl in tls:
        keys.append(tl)
        added += 1
    print("Added " + str(added) + " translations to list of keywords 'keys'")
    return keys


# Creates a list 'keys' containing user's keywords
def create_keys():
    global keys
    dir_Crawler(base)
    with open('keywords.csv', newline='') as f:
        for row in csv.reader(f):
            keys += row
    return keys


# Returns 'keyslist', a list of the user keys, their synonyms and translations
def extend_keyslist():
    global keyslist
    find_lemmas()
    find_translations()
    keyslist = remove_dups(keys)
    print("Created keyslist with " + str(len(keyslist)) + " keys")
    return keyslist


# =============================================================================
# Supporting information collection functions
# =============================================================================


# Main function for information collection
def collect_info():
    global keys
    # collects concordant text for keywords
    for word in keys:
        find_information(word)

    # Saves general case and contact information to dictionary and csv file
    find_contacts()


def find_information(word):
    global sentences
    info_all = []

    # search each sentence for the keyword
    for sentence in sentences:
        if word in sentence:
            info_all.append(sentence)    # returns 'info_all', a list of lists

    # save keyword-sentence pair to global dictionary
    case_info[word] = info_all

    # save info to csv
    store_data(case_info, path=(case + '_text.csv'))


# Stores data to a csv file in the case folder
def store_data(d, path):
    dir_case(base, case)
    with open(path, 'w', encoding="utf-8") as f:
        for key in d.keys():
            f.write("%s,%s\n" % (key, d[key]))
    print(path + ' created in case directory.')


# Collects contact information from scraped text
def find_contacts():
    for row in sentences:
        reg = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
        emails = re.findall(reg, row)
        if emails:
            case_info['contact'] = emails
            case_info['case name'] = case
            store_data(case_info, path=case + '_info.csv')
