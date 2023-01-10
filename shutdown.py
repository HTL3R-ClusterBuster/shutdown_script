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
    for server in read_from_file():
        print(url % server.strip())
        #requests.post((url % server), json=options)
        pass

def check_env():
    """
    checks if .env variables are configured
    :return dictionary with the env Variables
    """
    required = ['USER', 'PASSWORD']
    load_dotenv()
    for var in required:
        if not os.getenv(var):
            print(f'ERROR in .env! {var} is required but not configured.')
            sys.exit()
    return vars

if __name__ == '__main__':
    # check if env is configured correctly
    check_env()

    # call shutdown_server() method
    shutdown_servers()
