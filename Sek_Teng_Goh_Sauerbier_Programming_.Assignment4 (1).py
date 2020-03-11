# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 08:30:51 2020

@author: zhiting (sek teng)
"""
""" Webscraping
Scraping website : http://www.mind-and-brain.de/people/faculty/

The ‘Faculty’ page at the website for the Berlin School of Mind and Brain 
lists the school’s current faculty members. The purpose of the program
is to retrieve the details of faculty members from the current version of the 
web page and saves their information into a spreadsheet file. 

For each faculty member, all of the information that is displayed in their 
detail view (Function, Current status, Research area, etc.) are saved
in the CSV file, except for their phone number and email address. 

Encoding cp1252

"""
import requests
from bs4 import BeautifulSoup

# Create a new http session
session = requests.Session()

response = session.get('http://www.mind-and-brain.de/people/faculty/')#, headers=headers_firstpage)

doc = BeautifulSoup(response.text, 'html.parser')

fields_1 = doc.find_all("th")
fieldset = set() #removes duplicate items
for fielding in fields_1:
    fieldset.add(fielding.text)
fieldset.remove("E-mail")
fieldset.remove("Phone")#exclude email and phone 
print(fieldset)

results = doc.find_all("div",{"class":"researchers-list-item-full"})

with open("mind_brain_peeps.csv","w", encoding = "cp1252") as file:
    file.write("Name,") #1st row 1st column 
    for field_2 in fieldset:
        file.write(f"{field_2},") #write rows' headers 
    file.write("\n")#newline 

    for result in results: #loops through results with all researchers' items
        resultdict = {}
        
        resultdict['name'] = result.find("div",{"class","researchers-list-item-full-name"}).text.strip()

        #gets all the names in the results under this div class
        fields = result.find_all("tr")

        for field in fields:
            fieldname = f"{field.find('th').text.strip()}"
            fieldvalue = f"{field.find('td').text.strip()}"
            
            for c in fieldvalue: #going through line by line 
                if c == '"' :
                    fieldvalue = fieldvalue.replace(c, '\'')
                    #replace "" to ' so that text with quotations will not split up 
            
            resultdict[fieldname] = fieldvalue

        file.write(f"\"{resultdict['name']}\",")
        #writes first column 
        for field_ in fieldset: #loops through predetermined fieldset
            file.write(f"\"{resultdict.get(field_)}\",")
            #gets the value of the keys based on fieldset and write to csv
        file.write("\n")
        

