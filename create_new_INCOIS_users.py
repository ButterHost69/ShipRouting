import requests
import credentials


for email in credentials.INCOIS_EMAIL_LIST:
    header = {
        "Host": "sarat.incois.gov.in",
        "Cookie": "JSESSIONID=CF9EBA4CC9ABC820FC7736FD257231F2",
        "Content-Length": "95",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Chromium";v="127", "Not)A;Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Accept-Language": "en-US",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://sarat.incois.gov.in/",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://sarat.incois.gov.in/shipforecast/register.jsp",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i",
        "Connection": "keep-alive",
    }

    data = {
        "name":"Parth Kumar",
        "org":"GNU",
        "ship":"voyage",
        "email":f"{email}",
        "mobile":"6744067856",
        "password":"parthkumar"
    }
    url = "https://sarat.incois.gov.in/shipforecast/registerProcess.jsp"
    response = requests.post(url= url, headers= header, data=data)
    print(response.status_code)
    print(response.content)