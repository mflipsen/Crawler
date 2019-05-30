This program was created as part of my MSc Thesis project to obtain the degree of MSc Engineering & Policy Analysis of Delft University of Technology. The code in this program was either created by the author, or is (an adaptation of) open source code. 

# INPUT
The entire program contains the following scripts:
- run.py			    	# run the script to crawl and scrape for the case
- setup.py			    	# enter case name, and set preferences for the crawler
- crawler.py		  	    	# main script for crawling case websites
- googler.py		  	    	# supports crawler.py
- spider.py			    	# supports crawler.py
- link_finder.py		    	# supports spider.py
- domain.py	    	      		# supports crawler.py
- general.py	        		# supports crawler.py
- scraper.py	  	       		# main script for scraping crawled websites and processing data

Supporting (alterable) files:
- html.text_elements.csv		# supports scraper.py, can be changed by the user 

# OUTPUT
For each case, the program creates a directory containing folders for resp. the crawl and scrape output. 
The program output is stored as a docx-file in the case directory. As part of the content analysis, a word frequency plot is generated and stored in the case directory as well.



© 2019 Delft University of Technology
