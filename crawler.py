import threading
from queue import Queue
from spider import Spider
from domain import get_domain_name
from general import dir_crawled, file_to_set, create_project_dir
from setup import base, case, maxthreads
from googler import google_results, search_google

queue = Queue()
folder = case + '_crawler'

# =============================================================================
# Main crawler function for each search result
# =============================================================================


def crawl_case():

    # change cwd to store results under the case subfolders
    create_project_dir(folder)
    dir_crawled(base, case)

    # search google for the given query in setup.py
    search_google()
    print("google search complete")

    # for each google search result, crawl the urls
    for index, link in enumerate(google_results):

        # instantiate the Spider for the google results
        PROJECT_NAME = case + '_crawler' + str(index)
        HOMEPAGE = link
        DOMAIN_NAME = get_domain_name(HOMEPAGE)
        Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
        QUEUE_FILE = PROJECT_NAME + '/queue.txt'
        CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
        print(PROJECT_NAME, HOMEPAGE)

        # create threads that get the urls to the queue
        create_workers()
        crawl(QUEUE_FILE)


# =============================================================================
# Customized threading object
# =============================================================================

# adaptation of code from 
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch06s03.html


class myThread(threading.Thread):

    def __init__(self, threadID, name):
        """ constructor, setting initial variables """
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0

    def run(self):
        """ main control loop """
        print("Starting " + self.name)

        while not self._stopevent.isSet():
            work()
            self._stopevent.wait(self._sleepperiod)

        print("Exiting " + self.name)

    # currently not implemented, because of use of daemon threads
    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        threading.Thread.join(self, timeout)


# =============================================================================
# Supporting crawler functions
# =============================================================================

# the following code is an adaptation of code from
# https://github.com/AbdulSheikh/Spider/tree/master/Spider


# Create worker threads (will die when main exits)
def create_workers():
    for i in range(maxthreads):
        t = myThread(i, ("Thread-" + str(i)))
        t.setDaemon(True)
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs(QUEUE_FILE):
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()


# Check if there are items in the queue, if so crawl them
def crawl(QUEUE_FILE):
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs(QUEUE_FILE)
