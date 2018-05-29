#!/usr/bin/env python3

"""
Вспомогательная программа для прокси-сервера Squid
1. Читаем данные из входного потока и разбираем их согласно: https://wiki.squid-cache.org/Features/Redirectors
2. Читаем данные из файла JSON и если url имя совпало делаем перенеправление.
3. Пишем syslog.
"""
import sys
import syslog
import json
import re

#http://yandex.ru 172.17.8.175/saini.co.in - GET -
#([a-z]\w+.[a-z]{2,6})

#--------------------------------------------------
def url_clear(url):
    '''Очистка url адреса'''
    url = re.split(r"(^[a-z]\w+://)(www.)?", url)[-1]
    url = re.split(r"/", url)[0]

    #url = re.split(r"([a-z]\w+)", url)[1]
    #print(url)
    return url

#--------------------------------------------------
def loadingDataJSON():
    '''Загрузка данных из JSON файла'''
    with open('/etc/squid/dataweb.json') as f:
        data_json = f.read()
        dictValJOSN = json.loads(data_json)

    return dictValJOSN
#------------------------------------------------
def rewrite(url, ch_id, myip, myport):
    dictValJSON = loadingDataJSON()
    url = url_clear(url)
    for lineURL in dictValJSON.keys():
        if url.startswith(lineURL) :
            rewriteUrl = ch_id + ' OK status=301 url=https://' + dictValJSON[lineURL] + ' ' + myip + ' ' + myport + '\n'
            syslog.syslog(6, 'Squid_redirect from ' + url + ' to ' + dictValJSON[lineURL])
            #my_logger.debug('this is debug')
            print(rewriteUrl)
            break
    syslog.syslog(6, 'Squid_request_URL: ' + url)
    rewriteUrl = ch_id + ' ERR ' + myip + ' ' + myport + '\n'
    #print('rgequst')


    return rewriteUrl

#-------------------------------------------------
def main():
    while True:
        inRequest = sys.stdin.readline()
        try:
            [ch_id, url, ipaddr, ident, method, myip, myport] = inRequest.split()
        except ValueError:
            syslog.syslog(3, 'ValueError inRequest.split()')
            #print('error')
            continue
        outRequest = rewrite(url, ch_id, myip, myport)
        sys.stdout.write(outRequest)
        sys.stdout.flush()

# --------------------------------------------------
if __name__ == '__main__':
    main()
