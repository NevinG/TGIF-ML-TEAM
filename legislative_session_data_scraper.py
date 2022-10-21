import pandas as pd
import numpy as np
import requests
import json
from bs4 import BeautifulSoup

leg_sess = 79

while leg_sess <= 87:
    data = {}

    committee_names = {
    "Agriculture & Livestock": 0,
    "Appropriations": 1,
    "Appropriations-S/C on Criminal Justice": 2,
    "Appropriations-S/C on Education": 3,
    "Appropriations-S/C on General Government": 4,
    "Appropriations-S/C on Govt. Efficiency & Oper": 5,
    "Appropriations-S/C on Health & Human Services": 6,
    "Appropriations-S/C on Regulatory": 7,
    "Border & International Affairs": 8,
    "Business & Industry": 9,
    "Calendars": 10,
    "Civil Practices": 11,
    "Corrections": 12,
    "County Affairs": 13,
    "Criminal Jurisprudence": 14,
    "Culture, Recreation, & Tourism": 15,
    "Defense Affairs & State-Federal Relations    ": 16,
    "Economic Development": 17,
    "Election Contests, Select": 18,
    "Elections": 19,
    "Energy Resources": 20,
    "Environmental Regulation": 21,
    "Financial Institutions": 22,
    "General Investigating & Ethics": 23,
    "Government Reform": 24,
    "Higher Education": 25,
    "House Administration": 26,
    "Human Services": 27,
    "Insurance": 28,
    "Judiciary": 29,
    "Juvenile Justice & Family Issues": 30,
    "Land & Resource Management": 31,
    "Law Enforcement": 32,
    "Licensing & Administrative Procedures": 33,
    "Local & Consent Calendars": 34,
    "Local Government Ways & Means": 35,
    "Natural Resources": 63,
    "Pensions & Investments": 37,
    "Property Tax Relief, Select": 38,
    "Public Education": 39,
    "Public Education Reform, Select": 40,
    "Public Health": 41,
    "Redistricting": 42,
    "Regulated Industries": 43,
    "Rules & Resolutions": 44,
    "State Affairs": 67,
    "Transportation": 46,
    "Urban Affairs": 47,
    "Ways & Means": 48,
    "Administration": 49,
    "Business & Commerce": 50,
    "S/C on Emerging Technologies & Economic Dev.": 51,      
    "Criminal Justice": 52,
    "Education": 53,
    "Education Reform & Public School Finance, Sel": 54,
    "S/C on Higher Education": 55,
    "Finance": 56,
    "S/C on Capital Funding for Higher Education": 57,
    "Government Organization": 58,
    "Health & Human Services": 59,
    "Intergovernmental Relations": 60,
    "International Relations & Trade": 61,
    "Jurisprudence": 62,
    "S/C on Agriculture & Coastal Resources": 64,
    "S/C on Ag., Rural Affairs & Coastal Resources": 65,
    "Nominations": 66,
    "Transportation & Homeland Security": 68,
    "Veteran Affairs & Military Installations": 69,
    "S/C on Base Realignment and Closure": 70,   
    "Availability of Pre-Owned Heavy Duty Commercial Motor Vehicles, Study Commission on": 71,       
    "Medical Peer Review Process, Interim": 72,
    "Power of Eminent Domain, Interim": 73,
    "Texas Health Insurance Risk Pool Deficit, Interim": 74,
    "Transportation Financing": 75,
    "Windstorm Coverage & Budgetary Impact, Interim": 76
    }

    #add leg_sess to the data
    data["leg_sess"] = leg_sess

    #get house and senate numbers for the legislature
    #----------------------------------------------

    URL = 'https://lrl.texas.gov/sessions/memberStatistics.cfm'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    statistics_table = soup.findAll(lambda tag: tag.name=="table")[-(leg_sess - 73)]

    row = statistics_table.find(lambda tag: tag.name == 'td' and tag.text.find('Male') != -1).parent
    data['male_house_members'] = int(row.contents[3].text)
    data['male_senate_members'] = int(row.contents[5].text)

    row = statistics_table.find(lambda tag: tag.name == 'td' and tag.text.find('Female') != -1).parent
    data['female_house_members'] = int(row.contents[3].text)
    data['female_senate_members'] = int(row.contents[5].text)

    row = statistics_table.find(lambda tag: tag.name == 'td' and tag.text.find('Democrat') != -1).parent
    data['democrat_house_members'] = int(row.contents[3].text)
    data['democrat_senate_members'] = int(row.contents[5].text)

    row = statistics_table.find(lambda tag: tag.name == 'td' and tag.text.find('Republican') != -1).parent
    data['republican_house_members'] = int(row.contents[3].text)
    data['republican_senate_members'] = int(row.contents[5].text)

    row = statistics_table.find(lambda tag: tag.name == 'td' and tag.text.find('Incumbents') != -1).parent
    data['house_incumbents'] = int(row.contents[3].text)
    data['senate_incumbents'] = int(row.contents[5].text)

    row = statistics_table.find(lambda tag: tag.name == 'td' and tag.text.find('Freshmen') != -1).parent
    data['house_freshman'] = int(row.contents[3].text)
    data['senate_freshman'] = int(row.contents[5].text)

    row = statistics_table.find(lambda tag: tag.name == 'td' and tag.text.find('Under 30') != -1).parent
    data['house_members_age_under_30'] = int(row.contents[3].text)
    data['senate_members_age_under_30'] = int(row.contents[5].text)

    row = statistics_table.find(lambda tag: tag.name == 'td' and tag.text.find('30 - 39') != -1).parent
    data['house_members_age_30_to_39'] = int(row.contents[3].text)
    data['senate_members_age_30_to_39'] = int(row.contents[5].text)

    row = statistics_table.find(lambda tag: tag.name == 'td' and tag.text.find('40 - 49') != -1).parent
    data['house_members_age_40_to_49'] = int(row.contents[3].text)
    data['senate_members_age_40_to_49'] = int(row.contents[5].text)

    row = statistics_table.find(lambda tag: tag.name == 'td' and tag.text.find('50 - 59') != -1).parent
    data['house_members_age_50_to_59'] = int(row.contents[3].text)
    data['senate_members_age_50_to_59'] = int(row.contents[5].text)

    row = statistics_table.find(lambda tag: tag.name == 'td' and tag.text.find('60 - 69') != -1).parent
    data['house_members_age_60_to_69'] = int(row.contents[3].text)
    data['senate_members_age_60_to_69'] = int(row.contents[5].text)

    row = statistics_table.find(lambda tag: tag.name == 'td' and tag.text.find('70 and over') != -1).parent
    data['house_members_age_over_70'] = int(row.contents[3].text)
    data['senate_members_age_over_70'] = int(row.contents[5].text)


    #Get committee data
    URL = 'https://lrl.texas.gov/committees/cmtes.cfm?from=session&session={}'.format(leg_sess)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    def find_members_party(URL2):
        page2 = requests.get(URL2)
        soup2 = BeautifulSoup(page2.content, "html.parser")
        table2 = soup2.find(name="table")
        party = table2.findAll(name="tr")[5].findAll(name="td")[4].text
        if party.find('Republican') != -1:
            return 'republican'
        elif party.find('Democrat') != -1:
            return 'democrat'
        else:
            return 'other'

    def find_committee_stats(URL2):
        page2 = requests.get(URL2)
        soup2 = BeautifulSoup(page2.content, "html.parser")
        table2 = soup2.find(name="table")
        rows2 = table2.findAll(name='tr')[1].findAll(name='a')
        republican_count = 0
        democrat_count = 0

        for link in rows2:
            party = find_members_party('https://lrl.texas.gov/{}'.format(link.attrs['href']))
            if party == 'republican':
                republican_count+=1
            elif party == 'democrat':
                democrat_count+=1
        
        return republican_count, democrat_count



    table = soup.find(name="table")
    rows = list(map(lambda x: x, table.findAll(lambda tag: tag.name == 'a')))
    i = 0
    for link in rows:
        republican_count, democrat_count = find_committee_stats('https://lrl.texas.gov/committees/{}'.format(link.attrs['href']))
        data['committee_' + str(i) + "_republicans"] = republican_count
        data['committee_' + str(i) + "_democrats"] = democrat_count
        i +=1

    #print current data
    #-----------------------------
    #print (json.dumps(data, indent=2))


    df = pd.DataFrame(np.array([list(data.values())]), columns=list(data.keys()))
    df.to_csv('out.csv', mode='a')

    print(leg_sess, "done")
    leg_sess+=1
