import urllib.request
import os
import codecs
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import re

wordsfile = os.path.join(os.path.dirname(__file__), "words01.txt")
file1 = codecs.open(wordsfile, "r", "utf-8")
lines = file1.readlines()

urlbase = "https://www.merriam-webster.com/dictionary/"
  
count = 0
for word in lines:
    word = word.strip()
    htmlfile = os.path.join(os.path.dirname(__file__), "wordsHTML", word + ".html")
    txtfile = os.path.join(os.path.dirname(__file__), "wordsDefs", word + ".txt")
    print(word, end =" ")

    if os.path.exists(htmlfile):
        print (' exists')
        # continue

    url = urlbase + word;
    found = False

    try:
        page = urllib.request.urlopen(url)
    except HTTPError as e:
        print(' Error code: ', e.code)
        file1 = open("orphans.txt", "a")  # append mode
        file1.write(word + "\n")
        file1.close()
    except URLError as e:
        print('Reason: ', e.reason)
    else:
        found = True
    
    if found == True:
        pagehtml = page.read()
        htmlfile = os.path.join(os.path.dirname(__file__), "wordsHTML", word + ".html")

        file1 = codecs.open(htmlfile, "w", "utf-8")
        file1.write(str(pagehtml))
        file1.close()

        soup = BeautifulSoup(pagehtml, 'html.parser')

        text = soup.text
        file1 = codecs.open("htmltext.txt", "w","utf-8")  # append mode
        file1.write(text)
        file1.close()

        div_word = soup.find(class_ = 'row entry-header')

        if div_word:
            content = div_word.text

            txtfile = os.path.join(os.path.dirname(__file__), "wordsDefs", word + ".txt")
            file = codecs.open(txtfile, "w", "utf-8")
            file.write(content)

            divs = soup.find("div", {"class" : "sense-content w-100"})
            if divs:
                for div in divs:
                    content = "-----\n" + div.text
                    file.write(content)

            file.close()
        
        else:
            print(' no defs')
            file2 = open("nodefs.txt", "a")
            file2.write(word + "\n")
            file2.close()