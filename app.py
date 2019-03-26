import requests
import flask
from flask import request
from flask import Flask, make_response
import time
import json
import hashlib
import re
import xml.etree.ElementTree as ET
# 引入所需要的库
app = Flask(__name__)

#@app.route("/")
#return "Hello World!"
# 默认的

@app.route('/', methods=['GET'])

def wechat_tuling():
    if request.method == 'GET':
        #判断如果请求方式是get
        token = 'tulingrobot'
        # 这里输入你在微信公众号里面填的token
        my_signature = request.args.get('signature', '')
        # 获取携带 signature微信加密签名的参数
        my_timestamp = request.args.get('timestamp', '')
        # 获取携带 随机数timestamp的参数
        my_nonce = request.args.get('nonce', '')
        # 获取携带 时间戳nonce的参数
        my_echostr = request.args.get('echostr', '')
        # 获取携带 随机字符串 echostr的参数
        data = [token, my_timestamp, my_nonce]
        # 进行字典排序
        data.sort()
        temp = ''.join(data)
        # 拼接成字符串
        mysignature = hashlib.sha1(temp).hexdigest()
        # 将三个参数字符串拼接成一个字符串进行sha1加密
        if my_signature == mysignature:
            # 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
            res = make_response(my_echostr)
            res.headers['content-type'] = 'text'
            # 这段代码是为了避免微信token验证失败
            return res
        else:
            return ''

@app.route('/', methods=['POST'])

def autoreplay():

    xml = ET.fromstring(request.data)
    toUser = xml.find('ToUserName').text
    fromUser = xml.find('FromUserName').text
    msgType = xml.find("MsgType").text
    createTime = xml.find("CreateTime")
    if msgType == 'text':
        content = xml.find('Content').text
        content = reply(content)
        resp = make_response(reply_text(fromUser,
         toUser, reply(fromUser, content)))
        resp.headers['content-type'] = 'text'
        return resp
    else:
        return reply_text(fromUser, toUser, '暂不支持图片视频语音类')

def reply_text(to_user, from_user, content):
    """
    以文本类型的方式回复请求
    """
    return """
    <xml>
        <ToUserName><![CDATA[{}]]></ToUserName>
        <FromUserName><![CDATA[{}]]></FromUserName>
        <CreateTime>{}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{}]]></Content>
    </xml>
    """.format(to_user, from_user, int(time.time() * 1000), content)

def reply(info):
        # 定义一个对话机器人的函数
        api = 'http://openapi.tuling123.com/openapi/api/v2'
        # 请求api接口的网址
        data = {
            "perception": {
                "inputText": {
                    "text": info
                }
            },
            "userInfo": {
                "apiKey": "2644e8c88eda4ec48690881c2b59f672",
                "userId": 'amberjiang',
            }
        }
        # 请求的数据（这里只有对话的，可以添加url或者其他，有问题查看官方文档
        jsondata = json.dumps(data)
        # 根据官方文档，需要把利用json.dumps()方法把字典转化成json格式字符串
        response = requests.post(api, data=jsondata)
        # 发起post请求
        robot_res = json.loads(response.content)
        # 把json格式的数据再转化成Python数据输出
        return robot_res["results"][0]['values']['text']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
