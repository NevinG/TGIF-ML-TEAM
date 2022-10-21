import requests
from bs4 import BeautifulSoup

leg_sess = 79

data = {}

#get house and senate numbers for the legislature
#----------------------------------------------
URL = 'https://lrl.texas.gov/legeleaders/members/partyListSession.cfm?leg={}'.format(leg_sess)
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
chars = {'0','1','2','3','4','5','6','7','8','9'}

#get number of house democrats
house_democrats_index = soup.text.find('Democrats in the House of Representatives')
house_democrats = ""
started_finding_numbers = False
while(house_democrats_index < len(soup.text)):
    if soup.text[house_democrats_index] in chars:
        started_finding_numbers = True
        house_democrats += soup.text[house_democrats_index]
    elif started_finding_numbers:
        break
    house_democrats_index+=1
data["house_democrats"] = int(house_democrats)

#get number of house republicans
house_republicans_index = soup.text.find('Republicans in the House of Representatives')
house_republicans = ""
started_finding_numbers = False
while(house_republicans_index < len(soup.text)):
    if soup.text[house_republicans_index] in chars:
        started_finding_numbers = True
        house_republicans += soup.text[house_republicans_index]
    elif started_finding_numbers:
        break
    house_republicans_index+=1
data["house_republicans"] = int(house_republicans)

#get number of senate democrats
senate_democrats_index = soup.text.find('Democrats in the Senate')
senate_democrats = ""
started_finding_numbers = False
while(senate_democrats_index < len(soup.text)):
    if soup.text[senate_democrats_index] in chars:
        started_finding_numbers = True
        senate_democrats += soup.text[senate_democrats_index]
    elif started_finding_numbers:
        break
    senate_democrats_index+=1
data["senate_democrats"] = int(senate_democrats)

#get number of senate republicans
senate_republicans_index = soup.text.find('Republicans in the Senate')
senate_republicans = ""
started_finding_numbers = False
while(senate_republicans_index < len(soup.text)):
    if soup.text[senate_republicans_index] in chars:
        started_finding_numbers = True
        senate_republicans += soup.text[senate_republicans_index]
    elif started_finding_numbers:
        break
    senate_republicans_index+=1
data["senate_republicans"] = int(senate_republicans)


URL = 'https://lrl.texas.gov/sessions/memberStatistics.cfm'
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

statistics_table = soup.findAll(lambda tag: tag.name=="table")[-(leg_sess - 73)]
row = statistics_table.find(lambda tag: tag.name == 'td' and tag.text.find('Male') != -1)
pass

#print current data
#-----------------------------
import json
print (json.dumps(data, indent=2))

