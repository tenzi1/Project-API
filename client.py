import requests
import gspread
import datetime 
import json

url = 'http://127.0.0.1:8000/api/v1/upload/projects/'

headers = {
    'Content-Type': 'application/json'
}

def get_projects():
    gc = gspread.service_account()
    worksheet = gc.open('sample sheet').worksheet('Sheet1')
    rows = worksheet.get_all_records()
    projects = []
    for row in rows:
        project = {
            'title': row['Project Title'],
            'status': row['Project Status'],
            'donor': row['Donor'],
            'executing_agency': row['Executing Agency'],
            'implementing_partner': row['Implementing Partner'],
            'counterpar_ministry': row['Counterpart Ministry'],
            'type_of_assistance': row['Type of Assistance'],
            'budget_type': row['Budget Type'],
            'is_humanitarian': row['Humanitarian'] == 'Yes',
            'sector': row['Sector'],
            'commitments': row['Commitments'],
            'agreement_date': None if row['Agreement Date'] == '' else convert_date_string(row['Agreement Date']),
            'disbursement': row['Disbursement'],
            'disbursement_date':  None if row['Disbursement Date'] == '' else convert_date_string(row['Disbursement Date']),
            'municipality': {
            'name': row['Municipality'],
            'district': {
                'name': row['District'],
                    'province': {
                        'name': row['Province']
                    }
                    }
                }
            }
        projects.append(project)
    return projects


def convert_date_string(date_string):
    """
    Converts a date string in the format 'M/D/YYYY' to the format 'MM/DD/YYYY'
    """
    date = datetime.datetime.strptime(date_string, '%m/%d/%Y')
    return date.strftime('%m/%d/%Y')

# to post data
data = get_projects()
json_data = json.dumps(data)
response = requests.post(url, headers=headers, json=json_data )

