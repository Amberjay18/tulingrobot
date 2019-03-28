# -*- coding: utf-8 -*-
from flask import request
from flask import Flask, make_response
import hashlib

app = Flask(__name__)

@app.route("/")
# 这个就是对url的解析
# 也就是当你在前端访问一个网页在后端就会调用这个
# 修饰器下的函数
def index():
    return "Hello World!"

@app.route('/wechat', methods=['GET','POST'])
# route() 装饰器用于把一个函数绑定到一个 URL
# 所以在微信公众号修改配置那里，如果你写了“/wechat”在括号里，就要在url那里加上，不然就会token验证失败！
def wechat_tuling():
    if request.method == 'GET':

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
            # 开发者获得加密后的字符串可与signature对比，标识该请求来源微信
            return my_echostr
        else:
            return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)
    # 加上host这段，外网可以访问, 新浪SAE需要指定5050端口
