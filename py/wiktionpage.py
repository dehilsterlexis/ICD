import urllib.request
import os
import codecs
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import re

wordsfile = os.path.join(os.path.dirname(__file__), "orphans.txt")
file1 = codecs.open(wordsfile, "r", "utf-8")
lines = file1.readlines()

urlbase = "https://en.wiktionary.org/w/index.php?title="
urlsuffix = "&action=edit"
  
count = 0
for word in lines:
    word = word.strip()
    wiktionfile = os.path.join(os.path.dirname(__file__), "wiktionary", word + ".txt")
    print(word, end =" ")

    if os.path.exists(wiktionfile):
        print (' exists')
        # continue

    url = urlbase + word + urlsuffix;
    found = False

    try:
        page = urllib.request.urlopen(url)
    except HTTPError as e:
        print(' Error code: ', e.code)
        file1 = open("wikophans.txt", "a")  # append mode
        file1.write(word + "\n")
        file1.close()
    except URLError as e:
        print('Reason: ', e.reason)
    else:
        found = True
    
    if found == True:
        pagehtml = page.read()
        soup = BeautifulSoup(pagehtml, 'html.parser')
        wiktion_page = soup.find('textarea')

        if wiktion_page:
            pagetext = wiktion_page.text
            print(' found')
            file = codecs.open(wiktionfile, "w", "utf-8")
            file.write(word + '\n' + pagetext)
            file.close()
        
        else:
            print(' no defs')
            file2 = open("nopages.txt", "a")
            file2.write(word + "\n")
            file2.close()