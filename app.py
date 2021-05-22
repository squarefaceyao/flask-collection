from flask import Flask, jsonify, Markup, json, request
from db import DB
import threading, time

from job import  Job
"""
接口说明：
1 返回的是json数据

2 结构如下
{   
    resCode: 0, #非0即错误1
    data: #数据位置，一般为数组
    message: '本次请求的说明'
}
"""

app = Flask(__name__)
thr = Job()

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"



@app.route('/start_ad',methods=['GET', 'POST'])
def start_ad():
    table_name = request.get_json()['table_name']
    RF = request.get_json()['RF']
    type = request.get_json()['type']
    RF = int(RF)
    if request.method == 'POST' and type == 'submit':
        thr.resume()
        thr.run(table_name, RF)
    if request.method == 'POST' and type == 'pause':
        print('Stop collection')
        thr.pause()

    return '采集完成，请返回主页面'




@app.route('/headers', methods=['GET'])
def headers():
    resData = {
        "resCode": 0, # 非0即错误 1
        "data": [
            {"id":0, "text": 'Home', "url":'/'},
            {"id":1, "text": 'Collection', "url":'/collection'},
            {"id":2, "text": 'Datasets', "url":'/signal_tables'},
            {"id":3, "text": 'Help', "url":'/help'},

        ],# 数据位置，一般为数组
        "message": '对本次请求的说明'
    }
    return jsonify(resData)

@app.route('/signal_tables',methods=['GET','POST'])
def signal_tables():
    db = DB()
    arrdata = db.get_signal_values()
    # print(type(arrdata))

    resData = {
        "resCode": 0, #非0即错误1
        "data": arrdata,
        "message": '本次请求的说明'

    }

    return json.dumps(resData)



# post man
@app.route('/<string:table_name>', methods=['POST'])
def show_table(table_name):
    if request.method == 'POST':
        print("捕获到了post请求 table_name", table_name)
        get_data = json.loads(request.get_data(as_text=True))
        print("sssssss", get_data)
        key = get_data['key']
        print("key = ", key)
        secretKey = get_data['secretKey']
        db = DB()
        sql = 'select * from ' + table_name
        arrdata = db.chaxun(sql)
        # print(type(arrdata))
        resData = {
            "resCode": 0,  # 非0即错误1
            "data": arrdata,
            "message": '查询成功'

        }
        return jsonify(resData)
    else:
        resData = {
            "resCode": 1,  # 非0即错误1
            "data": [],
            "message": '请求方法错误'

        }
        return jsonify(resData)

def get_line(table_name):
    db = DB()
    sql = 'select * from '+ table_name
    datas = db.chaxun(sql)
    ad1 = [data['ad1'] for data in datas]
    ad2 = [data['ad2'] for data in datas]
    ad3 = [data['ad3'] for data in datas]
    ad4 = [data['ad4'] for data in datas]
    ad5 = [data['ad5'] for data in datas]
    ad6 = [data['ad6'] for data in datas]
    ad7 = [data['ad7'] for data in datas]
    ad8 = [data['ad8'] for data in datas]
    xdatas = [str(data['create_time']) for data in datas]
    return xdatas,ad1,ad2,ad3,ad4,ad5,ad6,ad7,ad8


@app.route('/show/<table_name>',methods=['POST'])
def show_myecharts(table_name):
    print('success:',table_name)
    xdatas,ad1,ad2,ad3,ad4,ad5,ad6,ad7,ad8=get_line(table_name)
    xdatas=Markup(json.dumps(xdatas)),
    ad1=json.dumps(ad1)
    ad2=json.dumps(ad2)
    ad3=json.dumps(ad3)
    ad4=json.dumps(ad4)
    ad5=json.dumps(ad5)
    ad6=json.dumps(ad6)
    ad7=json.dumps(ad7)
    ad8=json.dumps(ad8)

    resData = {
        "resCode": 0, #非0即错误1
        "data": [xdatas,ad1,ad2,ad3,ad4,ad5,ad6,ad7,ad8],
        "message": '本次请求的说明'

    }
    return resData

@app.route('/download/<table_name>',methods=['POST'])
def download(table_name):
    """
    成点击下载按钮，自动在浏览器下载。
    功能不是很完善，需要:param table_name:
    :return: 在static文件存放目录
    """
    db = DB()
    db.download("static",table_name)

    file=f'http://127.0.0.1:5000/static/mysql_{table_name}.csv'
    resData = {
        "resCode": 0,  # 非0即错误 1
        "data": file,  # 数据位置，一般为数组
        "message": '对本次请求的说明'
    }
    return jsonify(resData)










if __name__ == '__main__':
    print(__name__)
    app.run(debug=True)

