import requests
from bs4 import BeautifulSoup


bill = {
    "house_bill": False,
    "senate_bill": False,
    "bill_number": -1,
    "legislative_session": "",
    "primary_author": [],
    "joint_authors": [],
    "co_authors": [],
    "house_committee": "",
    "senate_committee": "",
    "subjects": "",
    "sponsor": "",
    "passed": False,

    "senate_democrats": 0,
    "senate_republicans": 0,
    "house_democrats": 0,
    "house_republicans": 0,
}

leg_sess = 79
bill_name = 'HB2'

#Data from history page
#--------------------------------------------
URL = 'https://capitol.texas.gov/BillLookup/History.aspx?LegSess={}R&Bill={}'.format(leg_sess,bill_name)
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

#get bill name details
billName = soup.find(id="usrBillInfoTabs_lblBill").text
bill["house_bill"] = billName.find("HB") != -1
bill["senate_bill"] = billName.find("SB") != -1
bill["bill_number"] = int(billName[3:])

#get bill legislative session
leg_session = soup.find(id="usrBillInfoTabs_lblItem1Data")
if leg_session:
    bill["legislative_session"] = leg_session.text

#get house committee
house_committee = soup.find(id="cellComm1Committee")
if house_committee:
    bill["house_committee"] = house_committee.text

#get senate committee
senate_committee = soup.find(id="cellComm2Committee")
if senate_committee:
    bill["senate_committee"] = senate_committee.text

#get subjects
subjects = soup.find(id="cellSubjects")
if subjects:
    bill["subjects"] = subjects.contents[::2]

#get sponsor
sponsor = soup.find(id="cellSponsors")
if sponsor:
    bill["sponsor"] = sponsor.text


#Data from authors page
#------------------------------------
URL = 'https://capitol.texas.gov/BillLookup/Authors.aspx?LegSess={}R&Bill={}'.format(leg_sess,bill_name)
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

#get primary author
primary_author = soup.find(id="tblPrimaryAuthors")
if primary_author:
    primary_author = primary_author.findAll(lambda tag: tag.name=='tr')[1].findAll(lambda tag: tag.name=='td')[0].text
    bill["primary_author"] = primary_author

#get joint authors
joint_authors = soup.find(id="tblJointAuthors")
if joint_authors:
    joint_authors = list(map(lambda x: x.findAll(lambda tag: tag.name=='td')[0].text, joint_authors.findAll(lambda tag: tag.name=='tr')[1:]))
    bill["joint_authors"] = joint_authors

#implement get co authors
co_authors = soup.find(id="tblCoauthors")
if co_authors:
    co_authors = list(map(lambda x: x.findAll(lambda tag: tag.name=='td')[0].text, co_authors.findAll(lambda tag: tag.name=='tr')[1:]))
    bill["co_authors"] = co_authors

#Data from bill stages page
#----------------------------------------------------
URL = 'https://capitol.texas.gov/BillLookup/BillStages.aspx?LegSess={}R&Bill={}'.format(leg_sess,bill_name)
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

#get whether bill passed or not
passed = soup.find(id="usrBillStages_pnlBillStages")
if passed:
    passed = passed.findAll(lambda tag: tag.name=='div' and tag.attrs['class'][0]=='stageText')
    passed = passed[-1]
    passed = passed.text.find('Bill becomes law.') != -1
    bill["passed"] = passed

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
bill["house_democrats"] = int(house_democrats)

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
bill["house_republicans"] = int(house_republicans)

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
bill["senate_democrats"] = int(senate_democrats)

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
bill["senate_republicans"] = int(senate_republicans)

#print current bill
#-----------------------------
import json

print (json.dumps(bill, indent=2))