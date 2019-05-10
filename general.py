import os
# import sys
import pickle
import contextlib
from pathlib import Path
from setup import case, query, maxresults, maxthreads, datetime


# Create a folder
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    with open(file_name, "w") as f:
        for l in sorted(links):
            f.write(l + "\n")


# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = os.path.join(project_name, 'queue.txt')
    crawled = os.path.join(project_name, "crawled.txt")
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# Pickle file
def pickle_file(path, data):
    with open(path, "wb") as filehandle:
        pickle.dump(data, filehandle)


# Create file with setup specifications
def create_setup():
    with open("setup.txt", "w") as file:
        file.write("# Directory settings" + '\n' +
                   "case = " + case + '\n' + '\n' +
                   "# Date and time of running program" + '\n' +
                   datetime + '\n' + '\n' +
                   "# Googler settings" + '\n' +
                   "query = " + query + '\n' +
                   "maxresults = " + str(maxresults) + '\n' + '\n' +
                   "# Crawler settings" + '\n' +
                   "maxthreads = " + str(maxthreads))


# Context manager to handle changes in directory
@contextlib.contextmanager
def cd(path):
    print('initially inside {0}'.format(os.getcwd()))
    if os.path.exists(path):
        os.chdir(path)
        # print('inside {0}'.format(os.getcwd()))
        try:
            yield
        except:
            # print('Exception caught: ', sys.exc_info()[0])
            pass
        finally:
            print('finally inside {0}'.format(os.getcwd()))


# Function to deploy the context manager
def change_cd(path):
    with cd(path):
        # print(os.listdir('.'))
        raise Exception('boom')


# Functions to use in program to change to specific directories
def dir_Crawler(base):
    change_cd(base)


def dir_case(base, case):
    change_cd(base)
    temp = Path.cwd().joinpath(case)
    change_cd(temp)


def dir_crawled(base, case):
    change_cd(base)
    temp = Path.cwd().joinpath(case)
    change_cd(temp)
    folder = case + '_crawler'
    temp1 = Path.cwd().joinpath(folder)
    change_cd(temp1)


def dir_scrapelist(base, case):
    change_cd(base)
    temp = Path.cwd().joinpath(case)
    change_cd(temp)
    folder = case + '_scraper'
    temp1 = Path.cwd().joinpath(folder)
    change_cd(temp1)
