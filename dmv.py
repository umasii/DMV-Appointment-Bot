# I'm not liable for any of this. Check readme.txt.
import requests
import time

services = ['Atlantic Center Mall', 'https://nysdmvqw.us.qmatic.cloud/qwebbook/rest/schedule/branches/c92d2048b00326a0d9452e478db504ce41ec8f67f8e008034295cbf85cf902df/services/10226f4de0f460aa67bb735db97f9eb434b8ac2a144e40a20ff1e1848ffbeae7/dates','Coney Island', 'https://nysdmvqw.us.qmatic.cloud/qwebbook/rest/schedule/branches/0b2bd54bb4e54eae475cf1b266cf85bec683771e5e231af74e292177ae5e2640/services/10226f4de0f460aa67bb735db97f9eb434b8ac2a144e40a20ff1e1848ffbeae7/dates']

while True:

    ACM = requests.get(services[1])
    CI = requests.get(services[3])
    print(ACM.text)
    print(CI.text)

    if ACM.ok != True:
        print('ACM ERROR')
    elif ACM.text != '[]':
        print(services[0] + ' available dates: ' + ACM.text)
    
    if CI.ok != True:
        print('CI ERROR')
    elif CI.text != '[]':
        print(services[2] + ' available dates: ' + CI.text)


    time.sleep(3600)