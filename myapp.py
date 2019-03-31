# -*- coding: utf-8 -*-
from flask import request
from flask import Flask, make_response
import xml.etree.ElementTree as ET
import hashlib
import requests, json, time


app = Flask(__name__)

@app.route("/")
# 这个就是对url的解析
# 也就是当你在前端访问一个网页在后端就会调用这个
# 修饰器下的函数
def index():
    return "Hello World!"

@app.route('/wechat', methods=['GET','POST'])
# route() 装饰器用于把一个函数绑定到一个 URL
# 所以在微信公众号修改配置那里，如果你写了“/wechat”在括号里，就要在url那里加上，不然会出现token验证失败的情况！
def wechat_tuling():
    if request.method == 'GET':
        if len(request.args) > 0:
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
            mysignature = hashlib.sha1(temp.encode('utf-8')).hexdigest()
            # # 判断请求来源，将三个参数字符串拼接成一个字符串进行sha1加密,这里注意转换成utf-8格式
            if my_signature == mysignature:
                # 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信

                return make_response(my_echostr)
            # 如果原样返回echostr的内容，则接入成功；否则接入失败
            else:
                return make_response('Access denied')
        else:
            return make_response('Wrong args received')

    else:
        # 下面是对请求解析，返回图灵机器人的回复

        xml = ET.fromstring(request.data)
        # 获取用户发送的原始数据
        # fromstring()就是解析xml的函数，然后通过标签进行find()，即可得到标记内的内容。
        toUser = xml.find('ToUserName').text
        # 获取之前发送的 目标用户（公众号）
        fromUser = xml.find('FromUserName').text
        # 获取之前的 消息来源用户
        msgType = xml.find("MsgType").text
        # 获取之前 向服务器发送的消息
        createTime = xml.find("CreateTime")
        if msgType == 'text':
            # 判断消息类型
            content = xml.find('Content').text
            return reply_text(fromUser,toUser, reply(fromUser, content))
        else:
            return reply_text(fromUser, toUser, '我还在学习其他知识，请等我慢慢成长！')

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
    app.run(host='0.0.0.0', port=5050)
    # 加上host这段，让其他用户可以访问你的服务, 新浪SAE需要指定5050端口
