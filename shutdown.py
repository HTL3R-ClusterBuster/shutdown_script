# Script shutdowns the servers which
# IDRAC IP addresses are listed in the
# file servers.txt

url = 'https://%s/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset'
options = {
    'ResetType': 'PushPowerButton'
}


def read_from_file():
    with open('./servers.txt') as f:
        for line in f:
            yield line


def shutdown_servers():
    for server in read_from_file():
        print(url % server.strip())
        #requests.post((url % server), json=options)
        pass


if __name__ == '__main__':
    shutdown_servers()
