from flask import Flask, jsonify
import requests
import csv
import multiprocessing
import os
import datetime
import json

app = Flask(__name__)

def precache_data():
    url = 'https://www.asx.com.au/asx/research/ASXListedCompanies.csv'
    data = requests.get(url, allow_redirects=True).content
    with open('asx.csv', 'wb') as f:
        f.write(data)
    with open('asx.csv', 'r', newline='') as f:
        csv_data = list(csv.reader(f))
    csv_data = [line[1] for line in csv_data[3:]]
    #test = list(map(get_data, csv_data))
    #for c in csv_data:
    #    get_data(c)
    with multiprocessing.Pool() as pool:
        pool.map(get_data, csv_data)

def get_data(company):
    filename = os.path.join('data', '{}_{}'.format(company, str(datetime.date.today())))
    if os.path.exists(filename):
        print('Skipping {}...'.format(filename))
        return True
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

@app.route('/')
def index():
    links = {
        "links" : {
            "self" : "/",
            "company" : "/company/<id>" 
        }
    }
    return jsonify(links)

@app.route('/company/<id>', methods=['GET']) 
def get_company_data(id):
    filename = os.path.join('data', '{}_{}'.format(id, str(datetime.date.today())))
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        if 'code' in data and 'primary_share' in data:
            return jsonify(data), 200
        else:
            raise requests.RequestException('Abnormal response: {}'.format(data))
    except Exception as ex:
        return jsonify('{}'.format(ex)), 404

""" @app.route('/company/<id>', methods=['GET']) 
def get_company_data(id):
    #html = requests.get('https://www.asx.com.au/asx/share-price-research/company/{}'.format(id)).text
    #soup = BeautifulSoup(html, 'html.parser')
    try:
        data = requests.get('https://www.asx.com.au/asx/1/company/{}'.format(id)).json()
        if 'code' in data and 'primary_share' in data:
            return jsonify(data), 200
        else:
            raise requests.RequestException('Abnormal response: {}'.format(data))
    except Exception as ex:
        return jsonify('{}'.format(ex)), 404 """

if __name__ == "__main__":
    precache_data()
    app.run(debug=True)

