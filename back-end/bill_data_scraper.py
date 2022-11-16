import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
from committee_dict import second_committee_to_number as committee_to_number
from os import path
import re
import time

leg_session_index = 0
leg_sessions = ['781', '782', '783', '784', '78R', '791', '792', '793', '79R', '80R', '811', '81R', '821', '82R', '831', '832', '833', '83R', '84R', '851', '85R', '86R', '871', '872', '873', '87R']
bill_name = 'HB'
bill_number = 1

df = None


#get starting info
print("Available Legislative Sessions: ")
leg_ses_dict = {i: leg_sessions[i] for i in range(len(leg_sessions))}
print (json.dumps(leg_ses_dict, indent=2))

leg_session_index = int(input("Enter legislative session:"))
stop_sess = int(input("Enter legislative session to stop at (inclusive):"))
bill_name = input("Enter 'HB' or 'SB':")
bill_number = int(input("Enter bill number to start at:"))

start = time.time()

times_in_row_failed_to_find_bill = 0
while leg_session_index <= stop_sess:
    
    bill = {
        "house_bill": False,
        "senate_bill": False,
        "bill_number": -1,
        "legislative_session": 0,
        "primary_author": [],
        "joint_authors": [],
        "co_authors": [],
        "house_committee": "",
        "senate_committee": "",
        "subjects": "",
        "sponsor": "",
        "passed": False,
    }

    #Data from history page
    #--------------------------------------------
    URL = 'https://capitol.texas.gov/BillLookup/History.aspx?LegSess={}&Bill={}{}'.format(leg_sessions[leg_session_index],bill_name,bill_number)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    
    if soup.text.find('The bill number does not exist for the selected legislative session.') != -1:
        if times_in_row_failed_to_find_bill < 10:
            times_in_row_failed_to_find_bill+=1
            bill_number+=1
            continue
        
        times_in_row_failed_to_find_bill = 0

        #save to csv
        if df is not None:
            end = time.time()
            print('session {}, {}, complete through bill {} --  time: {}'.format(leg_sessions[leg_session_index], bill_name, bill_number - 11, end - start))
            if not path.isfile('bill_data.csv'):
                df.to_csv('bill_data.csv', mode='a',index=False)
            else:
                df.to_csv('bill_data.csv', mode='a',index=False, header=False)
            df = None

            start = time.time()

        if bill_name == 'HB':
            bill_name = 'SB'
            bill_number = 1

        else:
            leg_session_index+=1
            bill_number = 1
            bill_name = 'HB'

        continue
    
    #get bill name details
    billName = soup.find(id="usrBillInfoTabs_lblBill").text
    bill["house_bill"] = billName.find("HB") != -1
    bill["senate_bill"] = billName.find("SB") != -1
    bill["bill_number"] = int(billName[3:])

    #get bill legislative session
    bill["legislative_session"] = leg_sessions[leg_session_index]

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
    URL = 'https://capitol.texas.gov/BillLookup/Authors.aspx?LegSess={}&Bill={}{}'.format(leg_sessions[leg_session_index],bill_name,bill_number)
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
    URL = 'https://capitol.texas.gov/BillLookup/Actions.aspx?LegSess={}&Bill={}{}'.format(leg_sessions[leg_session_index],bill_name,bill_number)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    #get whether bill passed or not
    passed = soup.findAll(name="table")[10]
    if passed:
        bill["passed"]  = passed.text.find('Reported enrolled') != -1

    #get session information
    leg_sess_df = pd.read_csv('leg_sess_data.csv')
    session_data = leg_sess_df.loc[leg_sess_df['leg_sess'] == int(leg_sessions[leg_session_index][:2])]

    bill["male_house_members"] = int(session_data.iloc[0]['male_house_members'])
    bill["male_senate_members"] = int(session_data.iloc[0]['male_senate_members'])
    bill["female_house_members"] = int(session_data.iloc[0]['female_house_members'])
    bill["female_senate_members"] = int(session_data.iloc[0]['female_senate_members'])
    bill["democrat_house_members"] = int(session_data.iloc[0]['democrat_house_members'])
    bill["democrat_senate_members"] = int(session_data.iloc[0]['democrat_senate_members'])
    bill["republican_house_members"] = int(session_data.iloc[0]['republican_house_members'])
    bill["republican_senate_members"] = int(session_data.iloc[0]['republican_senate_members'])
    bill["house_incumbents"] = int(session_data.iloc[0]['house_incumbents'])
    bill["senate_incumbents"] = int(session_data.iloc[0]['senate_incumbents'])
    bill["house_freshman"] = int(session_data.iloc[0]['house_freshman'])
    bill["senate_freshman"] = int(session_data.iloc[0]['senate_freshman'])
    bill["house_members_age_under_30"] = int(session_data.iloc[0]['house_members_age_under_30'])
    bill["senate_members_age_under_30"] = int(session_data.iloc[0]['senate_members_age_under_30'])
    bill["house_members_age_30_to_39"] = int(session_data.iloc[0]['house_members_age_30_to_39'])
    bill["senate_members_age_30_to_39"] = int(session_data.iloc[0]['senate_members_age_30_to_39'])
    bill["house_members_age_40_to_49"] = int(session_data.iloc[0]['house_members_age_40_to_49'])
    bill["senate_members_age_40_to_49"] = int(session_data.iloc[0]['senate_members_age_40_to_49'])
    bill["house_members_age_50_to_59"] = int(session_data.iloc[0]['house_members_age_50_to_59'])
    bill["senate_members_age_50_to_59"] = int(session_data.iloc[0]['senate_members_age_50_to_59'])
    bill["house_members_age_60_to_69"] = int(session_data.iloc[0]['senate_members_age_60_to_69'])
    bill["house_members_age_over_70"] = int(session_data.iloc[0]['house_members_age_over_70'])
    bill["senate_members_age_over_70"] = int(session_data.iloc[0]['senate_members_age_over_70'])

    bill["house_committee_democrats"] = int(session_data.iloc[0]['committee_{}_democrats'.format(committee_to_number.get(bill["house_committee"],0))])
    bill["house_committee_republicans"] = int(session_data.iloc[0]['committee_{}_republicans'.format(committee_to_number.get(bill["house_committee"],0))])
    bill["senate_committee_democrats"] = int(session_data.iloc[0]['committee_{}_democrats'.format(committee_to_number.get(bill["senate_committee"],0))])
    bill["senate_committee_republicans"] = int(session_data.iloc[0]['committee_{}_republicans'.format(committee_to_number.get(bill["senate_committee"],0))])


    #translate data to what were storing in the csv
    bill_data_for_csv = {
        "house_bill": bill["house_bill"],
        "senate_bill": bill["senate_bill"],
        "bill_number": bill["bill_number"],
        "legislative_session": bill["legislative_session"],
        #"party_of_primary_author": None,
        "num_of_joint_authors": len(bill['joint_authors']),
        "num_of_co_authors": len(bill["co_authors"]),
        "num_of_subjects": len(bill["subjects"]),
        #"party_of_sponsor": None,
        "passed": bill["passed"],
        "male_house_members": bill["male_house_members"],
        "male_senate_members": bill["male_senate_members"],
        "female_house_members": bill["female_house_members"],
        "female_senate_members": bill["female_senate_members"],
        "democrat_house_members": bill["democrat_house_members"],
        "democrat_senate_members": bill["democrat_senate_members"],
        "republican_house_members": bill["republican_house_members"],
        "republican_senate_members": bill["republican_senate_members"],
        "house_incumbents": bill["house_incumbents"],
        "senate_incumbents": bill["senate_incumbents"],
        "house_freshman": bill["house_freshman"],
        "senate_freshman": bill["senate_freshman"],
        "house_members_age_under_30": bill["house_members_age_under_30"],
        "senate_members_age_under_30": bill["senate_members_age_under_30"],
        "house_members_age_30_to_39": bill["house_members_age_30_to_39"],
        "senate_members_age_30_to_39": bill["senate_members_age_30_to_39"],
        "house_members_age_40_to_49": bill["house_members_age_40_to_49"],
        "senate_members_age_40_to_49": bill["senate_members_age_40_to_49"],
        "house_members_age_50_to_59": bill["house_members_age_50_to_59"],
        "senate_members_age_50_to_59": bill["senate_members_age_50_to_59"],
        "house_members_age_60_to_69": bill["house_members_age_60_to_69"],
        "house_members_age_over_70": bill["house_members_age_over_70"],
        "senate_members_age_over_70": bill["senate_members_age_over_70"],
        "house_committee_democrats": bill["house_committee_democrats"],
        "house_committee_republicans": bill["house_committee_republicans"],
        "senate_committee_democrats": bill["senate_committee_democrats"],
        "senate_committee_republicans": bill["senate_committee_republicans"]
    }

    #add to df
    if df is None:
        df = pd.DataFrame(np.array([list(bill_data_for_csv.values())]), columns=list(bill_data_for_csv.keys()))
    else:
        df2 = pd.DataFrame(np.array([list(bill_data_for_csv.values())]), columns=list(bill_data_for_csv.keys()))
        df = pd.concat([df, df2])

    

    #save to csv
    if df is not None:
        if bill_number % 100 == 0:
            end = time.time()
            print('session {}, {}, {} - {} complete  --  time: {}'.format(leg_sessions[leg_session_index], bill_name, bill_number - 100, bill_number, end - start))
            if not path.isfile('bill_data.csv'):
                df.to_csv('bill_data.csv', mode='a',index=False)
            else:
                df.to_csv('bill_data.csv', mode='a',index=False, header=False)
            df = None
            start = time.time()

    bill_number+=1

    #print current bill
    #-----------------------------
    # import json
    #print (json.dumps(bill_data_for_csv, indent=2))
