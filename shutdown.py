# Script shutdowns the servers which
# IDRAC IP addresses are listed in the
# file servers.txt
import argparse
import sys
import requests
import os
import logging
import urllib3

from dotenv import load_dotenv


# configure logger
logger = logging.getLogger()
formatter = logging.Formatter("%(asctime)s; %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
file_handler = logging.FileHandler('shutdown.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

# configure argparse
parser = argparse.ArgumentParser(
    prog='Shutdown script for Dell servers with IDRAC'
)
parser.add_argument("-s", "--start", action='store_true', dest="start", help="Explicitly starts server, not ")


# url to API shutdown route of the IDRAC Redfish API
url = 'https://%s/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset'

# power option for request json data
options = {
    'ResetType': 'PushPowerButton'
}

# get args
args = parser.parse_args()
if args.start:
    options = {
        'ResetType': 'On'
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
            logger.error(f'Error while connecting to server: {server} {e}')


def send_shutdown(session, address):
    """
    sends the API request
    :param session: the session with the AUTH data
    :param address: the address to send the request to
    :return:
    """
    response = session.post(address, json=options, timeout=5, verify=False)
    if response.status_code < 300:
        logger.info(f'Successfully send signal to {address}')
    else:
        logger.error(f'Request to {address} failed with status code {response.status_code}')


def check_env():
    """
    checks if .env variables are configured
    :return dictionary with the env Variables
    """
    load_dotenv()
    for var in required:
        if not os.getenv(var):
            logger.critical(f'Invalid .env! {var} is required but not configured.')
            sys.exit()
        else:
            env_vars[var] = os.getenv(var)


if __name__ == '__main__':
    # check if env is configured correctly
    logger.debug('Loading .env')
    check_env()

    # call shutdown_server() method
    logger.debug('Initiate Shutdown')
    shutdown_servers()
