from bs4 import BeautifulSoup
# import numpy as np
# import pandas as pd
# import bs4

with open("./index.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    

categories = soup.select('table[class="survey_table answerer"] div[class="survey_tab"]')

titles = []
for category in categories:
    titles.append(category.get_text(strip=True)[1:])
    
# for title in titles:
#     print(title)

questions_object = soup.find_all("div", {"class": "scope_additional_intro"})
# print(questions_object)
for question in questions_object:
    print(question.get_text(strip=True)[1:])
    

# questions_list = []
# for question in questions_object:
#     print(len())
    # questions_list.append(question)