import csv
from concurrent.futures import ThreadPoolExecutor
import requests
import os
import datetime
import json

def make_data_dir(path='data'):
    try:
        os.mkdir(path)
    except Exception as e:
        print(e)

def precache_all_data():
    url = 'https://www.asx.com.au/asx/research/ASXListedCompanies.csv'
    data = requests.get(url, allow_redirects=True).content
    with open('asx.csv', 'wb') as f:
        f.write(data)
    with open('asx.csv', 'r', newline='') as f:
        csv_data = list(csv.reader(f))
    csv_data = [line[1] for line in csv_data[3:]]
    make_data_dir()
    with ThreadPoolExecutor() as pool:
        pool.map(get_data, csv_data)

def get_today_str():
    return str(datetime.date.today())

def generate_filename(company, date_str=get_today_str(), folder='data'):
    return os.path.join(folder, '{}_{}'.format(company, date_str))

def get_data(company):
    filename = generate_filename(company)
    if os.path.exists(filename):
        print('Skipping {}...'.format(filename))
        return True
    make_data_dir()
    data = requests.get('https://www.asx.com.au/asx/1/company/{}?fields=primary_share'.format(company))
    json_data = data.json()
    if 'code' in json_data and 'primary_share' in json_data: 
        with open(filename, 'wb') as f:
            f.write(data.content)
        print(company)
        return True
    else:
        print('ERROR while processing {}'.format(company))
        print(json_data)
        return False

def open_file_and_return_data(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        if 'code' in data and 'primary_share' in data:
            return data, 200
        else:
            raise requests.RequestException('Abnormal response: {}'.format(data))
    except Exception as ex:
        return '{}'.format(ex), 404
