# Script shutdowns the servers which
# IDRAC IP addresses are listed in the
# file servers.txt
import sys

import requests
import os
from dotenv import load_dotenv

# url to API shutdown route of the IDRAC Redfish API
url = 'https://%s/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset'

# power option for request json data
options = {
    'ResetType': 'PushPowerButton'
}

# Name of the required ENV
required = ['USER', 'PASSWORD']

# ENV Dictionary
env_vars = {}


def read_from_file():
    """
    read all servers from file servers.txt
    :return: all IP addr in file
    """
    with open('./servers.txt') as f:
        for line in f:
            yield line


def shutdown_servers():
    """
    send the shutdown request for each server
    """
    session = requests.Session()
    session.auth = (env_vars.get('USER'), env_vars.get('PASSWORD'))
    for server in read_from_file():
        try:
            send_shutdown(session, (url % server.strip()))
        except Exception as e:
            print(f'Error while connecting to server: {server} \n{e}')


def send_shutdown(session, address):
    """
    sends the API request
    :param session: the session with the AUTH data
    :param address: the address to send the request to
    :return:
    """
    response = session.post(address, json=options, timeout=5)
    if response.status_code < 300:
        print(f'Successfully send signal to {address}')
    else:
        print(f'Request to {address} failed with status code {response.status_code}')


def check_env():
    """
    checks if .env variables are configured
    :return dictionary with the env Variables
    """
    load_dotenv()
    for var in required:
        if not os.getenv(var):
            print(f'ERROR in .env! {var} is required but not configured.')
            sys.exit()
        else:
            env_vars[var] = os.getenv(var)


if __name__ == '__main__':
    # check if env is configured correctly
    check_env()

    # call shutdown_server() method
    shutdown_servers()
