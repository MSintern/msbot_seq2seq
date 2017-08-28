#coding=utf-8
from flask import Flask, render_template, request, make_response
from flask import jsonify
import json

import seq2seq

import hashlib
import xml.etree.ElementTree as ET

from flask import Flask, request,make_response
import time



try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

app = Flask(__name__,static_url_path="/static")
#app.debug = True


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        token = 'wechat123'  # 自定义微信配置所需的token
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        s=s.encode('utf8')
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    if request.method == 'POST':
        xml = ET.fromstring(request.data)
        toUser = xml.find('ToUserName').text
        fromUser = xml.find('FromUserName').text
        msgType = xml.find("MsgType").text
        createTime = xml.find("CreateTime")
        if msgType == "text":
            content = xml.find('Content').text
            req_msg=content
            res_msg=seq2seq.decode_line(sess,model,req_msg)
            return reply_text(fromUser, toUser, res_msg)
        else:
            return reply_text(fromUser, toUser, "我们可以愉快地聊天了！请输入文本～")


def reply_text(to_user, from_user, content):
    """
    以文本类型的方式回复请求
    :param to_user:
    :param from_user:
    :param content:
    :return:
    """
    return """
    <xml>
        <ToUserName><![CDATA[{}]]></ToUserName>
        <FromUserName><![CDATA[{}]]></FromUserName>
        <CreateTime>{}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{}]]></Content>
    </xml>
    """.format(to_user, from_user,
               int(time.time() * 1000),
               content)



@app.route('/message', methods=['POST'])
def response():
    req_msg = request.form['msg']
    res_msg = seq2seq.decode_line(sess, model, req_msg)
    return jsonify( { 'text': res_msg } )



@app.route("/")
def index():
    return render_template("index.html")


import tensorflow as tf
import seq2seq
sess = tf.Session()
sess, model = seq2seq.init_session(sess)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)











