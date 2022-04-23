#importing packages
from pandas.io import html
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

#opening the input excel file containing links
links = pd.read_excel("Input.xlsx", engine="openpyxl")

#defining function to extract useful text from links
def extractText(links):
    i = 1
    for link in links.URL:

        #for mod security error
        user = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246 '}
        
        url = str(link)
        r = requests.get(url, headers= user)
        htmlContent = r.content
        
        soup = BeautifulSoup(htmlContent, "html.parser")

        #for unicode error

        for para in soup.find_all('div', class_='td-post-content'): #becuase all useful content is in td-post-content

            #making files as URL_ID
            with open(os.path.join("text_files", f"{i}.txt"), 'w', encoding="utf-8") as f:
                f.write(soup.title.string)
                f.write(para.get_text())
        print(f"{i}.txt created")
        i += 1

        
extractText(links)
