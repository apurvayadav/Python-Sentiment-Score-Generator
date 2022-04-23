# Python-Sentiment-Score-Generator

##Introduction
A Python Sentiment Score Generator takes a Input .xlsx file with links from a data science blog website- "Blackcoffer" and saves the content of the webpages in text file. Then By using nltk library Sentiment scores arfe generated and saved in an Output .csv file.

## [Input.xlsx](https://github.com/apurvayadav/Python-Sentiment-Score-Generator/blob/main/Input.xlsx)
This file contains 35 links from the Blackcoffer website.

## [text_extraction.py](https://github.com/apurvayadav/Python-Sentiment-Score-Generator/blob/main/text_extraction.py)
Python file containing the code to extract the content from the links and save it to text files in the [text_files](https://github.com/apurvayadav/Python-Sentiment-Score-Generator/tree/main/text_files) using BeautifulSoup, Pandas, requests and os module.

## [text_analysis.py](https://github.com/apurvayadav/Python-Sentiment-Score-Generator/blob/main/text_analysis.py)
This program uses the nltk library to Generate scores like posiitve_score, polarity_score, fog_index of the content in the text files. And saves the out in the [Output.csv](https://github.com/apurvayadav/Python-Sentiment-Score-Generator/blob/main/Output.csv) file.

## Demonstration
You can check out the demonstration of this project on my linkedIn profile at this [link]
