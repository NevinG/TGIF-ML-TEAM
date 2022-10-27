import requests
import difflib
import json
from bs4 import BeautifulSoup

#gets all the committee names from first site
def get_committee_names (first_session=71, last_session=87):
    committee_names = set()
    while first_session <= last_session:
        URL = 'https://lrl.texas.gov/committees/cmtes.cfm?from=session&session={}'.format(first_session)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        table = soup.find(name="table")
        rows = list(map(lambda x: x, table.findAll(lambda tag: tag.name == 'a')))
        for link in rows:
            committee_names.add(link.text)

        first_session +=1
    
    return committee_names

#gets all the committee names from the second site
def get_committee_names_2 ():
    with open('committee_names.txt', 'r') as file: 
        committee_names = set()
        for line in file:
            if line.strip():
                committee_names.add(line.strip())

    return committee_names

first_committee_names = get_committee_names()
second_committee_names = get_committee_names_2()

first_committee_to_number = {}
second_committee_to_number = {}

i = 0
for name in first_committee_names:
    first_committee_to_number[name] = i
    i+=1

for name in second_committee_names:
    newName = name.replace(' & ', ' and ')
    newName = newName.replace(' S/C ', 'Subcommittee')

    closest_name = difflib.get_close_matches(newName, first_committee_names, 1, 0)[0]
    second_committee_to_number[name] = first_committee_to_number[closest_name]
