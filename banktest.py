import requests
from requests.auth import HTTPBasicAuth
import base64
import json

#urls
url_token = 'https://doob.world:6442/v1/auth/token?grant_type=client_credentials'
url_acc_list = 'https://doob.world:6442/v1/accounts'
url_acc_balance = 'https://doob.world:6442/v1/accounts/{account}/balance'
url_acc_details = 'https://doob.world:6442/v1/accounts/{account}/'
url_acc_name = 'https://doob.world:6442/v1/accounts/{account}/name?bank=050000'

url_acc_statement = 'https://doob.world:6442/v1/statements/{account}'
url_acc_statement_date = 'https://doob.world:6442/v1/statements/{account}?from={Startdate}&to={Enddate}&'
url_acc_statement_page = 'https://doob.world:6442/v1/statements/{account}?from={Startdate}&to={Enddate}&page={a}&size={b}'         1231212
url_acc_statement_rec = 'https://doob.world:6442/v1/statements/{account}?&record={c}'
url_acc_statement_rec_page = 'https://doob.world:6442/v1/statements/{account}?&page={a}&size={b}&record={c}'

url_dom_transfer = 'https://doob.world:6442/v1/transfer/domestic'

#accs
acc1, acc2 = 5123085810, 5447305861
header = dict()


def get_token():
    '''Test function to get token
        returns : (str)token
    '''
    head = {'Content-Type':'application/x-www-form-urlencoded'}
    name = '7drM987FffPt6kmfEu9It1E2cd6OmvGO'
    pwd = 'mamVBAB0r5tuGv5u'
    response = requests.post(url_token, auth=HTTPBasicAuth(name, pwd), headers=head)
    token = response.json()['access_token']
    return token


def get_acc_list(token):
    '''Test function to get acc list
        args: (str)token
        returns : (list)accounts
    '''
    header["Authorization"] = "Bearer " + token
    print(header)
    response = custom_request(url_acc_list, header)
    return response['accounts']


def get_acc_balance(token, account):
    '''Test function to get acc balance
        args:
            (str)token
            (int)account
        returns : (dict)balance
    '''
    url = url_acc_balance.format(account = str(account))
    header["Authorization"] = "Bearer " + token
    response = custom_request(url, header)
    return response


def get_acc_details(token, account):
    '''Test function to get acc balance
        args:
            (str)token
            (int)account
        returns : (dict)details
    '''
    url = url_acc_details.format(account = str(account))
    header["Authorization"] = "Bearer " + token
    response = custom_request(url, header)
    return response


def get_acc_name(token, account):
    '''Test function to get acc balance
        args:
            (str)token
            (int)account
        returns : (dict)name
    '''
    url = url_acc_name.format(account = str(account))
    header["Authorization"] = "Bearer " + token
    response = custom_request(url, header)
    return response


def get_acc_statement(token, account, start_date = '', end_date = '',
                      record = '', page = '', page_line = ''):
    '''Test function to get acc balance
        args:
            (str)token
            (int)account
            (int)start_date ->YYYYMMDD
            (int)end_date ->YYYYMMDD
            (int)record 
            (int)page
            (int)page_line
        returns : (dict)acc_statement
    '''
    #print(account , start_date, end_date, record, page, page_line)
    if((bool(start_date) or bool(end_date)) and not bool(page)):
        print("1")
        url = url_acc_statement_date.format(account = str(account), Startdate = str(start_date), Enddate = str(end_date))
    elif(not bool(record) and (bool(start_date) or bool(end_date) and bool(page) and bool(page_line))):
        print("2")
        url = url_acc_statement_page.format(account = str(account), Startdate = str(start_date),
                                            Enddate = str(end_date), a = str(page), b = str(page_line))
    elif(bool(record) and not bool(page)):
        print("3")
        url = url_acc_statement_rec.format(account = str(account), c = str(record))
    elif(bool(record) and bool(page) and bool(page_line)):
        print("4")
        url = url_acc_statement_rec_page.format(account = str(account), a = str(page), b = str(page_line), c = str(record))
    else:
        print("5")
        url = url_acc_statement.format(account = str(account))
    header["Authorization"] = "Bearer " + token
    response = custom_request(url, header)
    return response


def domestic_trasnfer(url, token):
    '''Test function to get acc balance
        args:
            (str)url
            (str)token
        returns : (dict)acc_statement
    '''
    headers = {"Content-Type": "application/json",
               "Authorization": 'Bearer ' + token}
    headers = json.dumps(headers) # making sure it's really a json format, works without it
    pwd = base64.b64encode("8jnbmunh".encode('utf-8')).decode('utf-8') #password encoding
    #print(pwd)
    data = {"fromAccount": "5123085810",
            "toAccount": "5447305861",
            "amount": 123.00,
            "description": "TEST",
            "currency": "MNT",
            "transferid": "1471",
            "loginName": "fmconsulting",
            "tranPassword": pwd,
           }
    data = json.dumps(data) # making sure it's really a json format, works without it
    response = requests.post(url, headers, json=data)
    print(response.text)

def custom_request(url, headers, post = False):
    ''' Custom request function
        post = True -> post method
        post = False -> get method
    '''
    try:
        response = requests.post(url, headers = header) if post else requests.get(url, headers = header)
    except Exception as e:
        raise
    else:
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
            

token = get_token()
l = get_acc_list(token)
bal = get_acc_balance(token, acc1)
det = get_acc_details(token, acc1)
name = get_acc_name(token, acc1)
get_acc_statement(token, acc1)
get_acc_statement(token, acc1, start_date = 20211010)
get_acc_statement(token, acc1, end_date = 20211010)
get_acc_statement(token, acc1, start_date = 20211010, end_date = 20211011)
get_acc_statement(token, acc1, start_date = 20211010, end_date = 20211011, page = 5, page_line = 10)
get_acc_statement(token, acc1, record = 1000, page = 5, page_line = 10)
get_acc_statement(token, acc1, record = 1000)

domestic_trasnfer(url_dom_transfer, token)
