# I'm not liable for any of this. Check readme.txt.
import requests
import time
from datetime import date
print(date.today())

session = requests.Session()

acmbranch = 'c92d2048b00326a0d9452e478db504ce41ec8f67f8e008034295cbf85cf902df'
cibranch = '0b2bd54bb4e54eae475cf1b266cf85bec683771e5e231af74e292177ae5e2640'
test = '10226f4de0f460aa67bb735db97f9eb434b8ac2a144e40a20ff1e1848ffbeae7'

def constructurl(b,s):
    dateurl = 'https://nysdmvqw.us.qmatic.cloud/qwebbook/rest/schedule/branches/' + b + '/services/' + s + '/dates'
    return dateurl

def getdates(b,s):
    dates = requests.get(constructurl(b,s))
    date = eval(dates.text)[0]
    return date["date"]

def gettimes(b,s,d):
    times = requests.get(constructurl(b,s)+'/'+d+'/times')
    return times.text

def constructpath(b,s,d,t):
    path = '/qwebbook/rest/schedule/branches/' + b + '/services/' + s + '/dates'+'/'+d+'/times/'+t+'/reserve'
    return path

def reserve(b,s,d,t):
    path = constructpath(b,s,d,t)
    data = '{"appointment" : {"customers":[], "resources":[]}}'
    headers = {
        "authority": 'nysdmvqw.us.qmatic.cloud',
        "method": 'POST',
        "path": path,
        "scheme": 'https',
        "accept": 'application/json, text/javascript, */*; q=0.01',
        "accept-encoding": 'gzip, deflate, br',
        "accept-language": 'en-US,en;q=0.9',
        "content-type": 'application/json',
        "cookie": 'JSESSIONID='+cookies["JSESSIONID"],
        "origin": 'https://nysdmvqw.us.qmatic.cloud',
        "referer": 'https://nysdmvqw.us.qmatic.cloud/qwebbook/index.jsp',
        "sec-fetch-dest": 'empty',
        "sec-fetch-mode": 'cors',
        "sec-fetch-site": 'same-origin',
        "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        "x-requested-with": 'XMLHttpRequest'
    }
    reserveurl = session.post(constructurl(b,s)+'/'+d+'/times/'+t+'/reserve', headers = headers, data = data)
    return reserveurl.text

def confirm(p):
    today = date.today()
    headers = {
    'authority': 'nysdmvqw.us.qmatic.cloud',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'content-type': 'application/json',
    'origin': 'https://nysdmvqw.us.qmatic.cloud',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://nysdmvqw.us.qmatic.cloud/qwebbook/index.jsp',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'JSESSIONID='+cookies["JSESSIONID"],
    }
    data = '{"appointmentReference":"","title":"","customer":{"firstName":'+firstname+',"lastName":'+lastname+',"dateOfBirth":"'+str(today)+'","email":'+email+',"phone":"'+phone+'","externalId":""},"notes":"","languageCode":"en-US","notificationType":""}'
    response = requests.post('https://nysdmvqw.us.qmatic.cloud/qwebbook/rest/schedule/appointments/'+p+'/confirm', headers=headers, data=data)
    print(data)
    print('https://nysdmvqw.us.qmatic.cloud/qwebbook/rest/schedule/appointments/'+p+'/confirm')
    print(response.text)
    print(response)

if __name__ == "__main__":
    while True:
        try:
            ACM = requests.get(constructurl(acmbranch,test))
            CI = requests.get(constructurl(cibranch,test))

            print(ACM.text)
            print(CI.text)

            if not ACM.ok:
                print('ACM ERROR')
            elif ACM.text != '[]':
                print('ACM available dates: ' + ACM.text)
                while True:
                    try:
                        index = requests.get('https://nysdmvqw.us.qmatic.cloud/naoa/index.jsp')
                        cookies = index.cookies.get_dict()
                        print(cookies["JSESSIONID"])
                        datee = getdates(acmbranch,test)
                        print(datee)
                        times = gettimes(acmbranch,test,datee)
                        print(times)

                        timelist = eval(times)
                        print(timelist)
                        timee = timelist[round(len(timelist)/2)-1]
                        print(timee)
                        timestr = timee["time"]
                        print(timestr)
                        reservelist = reserve(acmbranch,test,datee,timestr)
                        print(reservelist)
                        publicid = reservelist.split('":"')[22][:-2]
                        print(publicid)
                        confirm(publicid)
                        break
                    except Exception:
                        print("An error occurred... Retrying.")
                break

            if not CI.ok:
                print('CI ERROR')
            elif CI.text != '[]':
                print('CI available dates: ' + CI.text)
                while True:
                    try:
                        index = requests.get('https://nysdmvqw.us.qmatic.cloud/naoa/index.jsp')
                        cookies = index.cookies.get_dict()
                        print(cookies["JSESSIONID"])
                        datee = getdates(cibranch,test)
                        print(datee)
                        times = gettimes(cibranch,test,datee)
                        print(times)

                        timelist = eval(times)
                        print(timelist)
                        timee = timelist[round(len(timelist)/2)-1]
                        print(timee)
                        timestr = timee["time"]
                        print(timestr)
                        reservelist = reserve(cibranch,test,datee,timestr)
                        print(reservelist)
                        publicid = reservelist.split('":"')[22][:-2]
                        print(publicid)
                        confirm(publicid)
                        break
                    except:
                        print("An error occurred... Retrying.")
                break

            time.sleep(3600)
        except Exception:
            print("An error occurred... Retrying.")