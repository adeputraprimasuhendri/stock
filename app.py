import csv
import time
import urllib.request as urllib2
import codecs
from datetime import datetime
import random

from flask import Flask, jsonify, request
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)
sock.init_app(app)

@sock.route('/stock')
def stock():
    while True:
        stcd = 'BBCA'
        from_date = '1624320000'
        to_date = '1655856000'
        interval = '1d'
        url = 'https://query1.finance.yahoo.com/v7/finance/download/' + stcd + '.JK?period1=' + str(
            from_date) + '&period2=' + str(to_date) + '&interval=' + interval + '&events=history'
        response = urllib2.urlopen(url)
        cr = csv.reader(codecs.iterdecode(response, 'utf-8'))
        next(cr)
        for row in cr:
            n = random.randint(0, 100)
            data = {
                "open": int(float(row[1])),
                "high": int(float(row[2])),
                "low": int(float(row[3])),
                "close": int(float(row[4])) + n,
                "volume": int(float(row[6])) + n
            }
            ws.send(data)
            time.sleep(1)


@app.route('/history', methods=['GET'])
def history():
    args = request.args
    stcd = args.get("code")
    from_date = to_integer(args.get("from"))
    to_date = to_integer(args.get("to"))
    interval = args.get("interval")
    url = 'https://query1.finance.yahoo.com/v7/finance/download/'+stcd+'.JK?period1='+str(from_date)+'&period2='+str(to_date)+'&interval='+interval+'&events=history'
    response = urllib2.urlopen(url)
    cr = csv.reader(codecs.iterdecode(response, 'utf-8'))
    next(cr)
    data=[]
    for row in cr:
        data.append({
            "date":to_integer(row[0]),
            "open": int(float(row[1])),
            "high": int(float(row[2])),
            "low": int(float(row[3])),
            "close": int(float(row[4])),
            "volume": int(float(row[6]))
        })
    return jsonify({"code" : stcd, "data": data, "from": from_date, "to":to_date})

def to_integer(dt_time):
    return int(datetime.timestamp(datetime.strptime(dt_time, '%Y-%m-%d')))