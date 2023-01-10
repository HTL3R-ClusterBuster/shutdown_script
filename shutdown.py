# Script shutdowns the servers which
# IDRAC IP addresses are listed in the
# file servers.txt
import requests

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
        requests.post((url % server), json=options)
        pass


if __name__ == '__main__':
    # call shutdown_server() method
    shutdown_servers()
