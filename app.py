import csv
import urllib.request as urllib2
import codecs
from datetime import datetime

from flask import Flask, jsonify, request
app = Flask(__name__)

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