import json
from prettytable import PrettyTable

import requests

URL = 'http://127.0.0.1:8000/rate/'
URL2 = 'http://127.0.0.1:8000/'


def client():
    while True:
        print('Write your command:')
        command = input()
        args = command.split(' ')
        if args[0] == 'register':
            register(args)
        elif len(args) == 2 and args[0] == 'login' and args[1] == URL2:
            login(args)
        elif args[0] == 'logout':
            logout(args)
        elif args[0] == 'list':
            list_all(args)
        elif args[0] == 'view':
            view(args)
        elif len(args) == 3 and args[0] == 'average':
            aver(args)
        elif len(args) == 6 and args[0] == 'rate':
            rate(args)
        elif args[0] == 'q':
            print('bye~')
            return 0
        else:
            print('invalid command.')
        continue


def register(args):
    print('Write your username:')
    username = input()
    print('Write your password:')
    password = input()
    print('Write your email:')
    email = input()
    request = {
        'username': username,
        'password': password,
        'email': email
    }
    response = requests.post(URL + 'register', request)
    message = json.loads(response.text).get('message')
    print(message)


def login(args):
    print('Write your username:')
    username = input()
    print('Write your password:')
    password = input()
    request = {
        'username': username,
        'password': password,
    }
    response = requests.post(URL + 'login', request)
    message = json.loads(response.text).get('message')
    global TOKEN
    global USERNAME
    TOKEN = json.loads(response.text).get('token')
    USERNAME = username
    print(message)


def logout(args):
    request = {
        'token': TOKEN,
        'username': USERNAME
    }
    response = requests.post(URL + 'logout', request)
    message = json.loads(response.text).get('message')

    print(message)


def list_all(args):
    request = {}
    response = requests.post(URL + 'list', request)

    rows = json.loads(response.text).get('list')

    tb = PrettyTable()
    tb.field_names = ['Code', 'Name', 'Year', 'Semester', 'Taught by']

    tmp = 0
    for row in rows[0]:
        if row.get('id') == tmp:
            tb.add_row(['', '', '', '', row.get('taught_by__code') + ', ' + row.get('taught_by__name')])
        else:
            tb.add_row([row.get('code'), row.get('name'), row.get('year'), row.get('semester'),
                        row.get('taught_by__code') + ', ' + row.get('taught_by__name')])
        tmp = row.get('id')
    print(tb)


def view(args):
    request = {}
    response = requests.post(URL + 'view', request)

    rows = json.loads(response.text).get('list')
    for row in rows:
        print('The rating of ' + row.get('name') + '(' + row.get('code') + ') is ' + str(row.get('rate')))


def aver(args):
    request = {
        'professor': args[1],
        'course': args[2]
    }
    response = requests.post(URL + 'average', request)

    row = json.loads(response.text)

    print('The rating of ' + row.get('professor') + '(' + row.get('id') +
          ') in module ' + row.get('course') + '(' + row.get('code') + ') is ' + str(row.get('rate')))


def rate(args):
    request = {
        'professor': args[1],
        'course': args[2],
        'year': args[3],
        'semester': args[4],
        'rate': args[5],
        'token': TOKEN
    }
    response = requests.post(URL + 'rate', request)

    message = json.loads(response.text).get('message')

    print(message)


if __name__ == '__main__':
    client()
