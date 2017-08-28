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


@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        if 'msg' in request.args:
            req_msg = request.args['msg']
            res_msg = seq2seq.decode_line(sess, model, req_msg)
            return res_msg
        else:
            return bad_msg()
    elif request.method == 'POST':
        if 'Content-Type' in request.headers:
            if request.headers['Content-Type'] == 'application/json':
                json_ = request.get_json()
                if 'msg' in json_:
                    res_msg = seq2seq.decode_line(sess, model, json_['msg'])
                    return res_msg
                else:
                    return bad_msg()

            elif request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
                req_msg = request.form['msg']
                if req_msg == None:
                    return bad_msg()
                else:
                    res_msg = seq2seq.decode_line(sess, model, req_msg)
                    return res_msg

            elif request.headers['Content-Type'] == '':
                str_data = request.get_data().decode('ascii')
                dict_data = json.loads(str_data)
                if 'msg' in dict_data:
                    res_msg = seq2seq.decode_line(sess, model, dict_data['msg'])
                    return res_msg
                else:
                    return bad_msg()

            else:
                return bad_contentType()
        else:
            str_data = request.get_data().decode('ascii')  # python3.5 need decode. 2.7 3.6 no need

            dict_data = json.loads(str_data)

            if 'msg' in dict_data:
                res_msg = seq2seq.decode_line(sess, model, dict_data['msg'])
                return res_msg
            else:
                return bad_msg()

    else:
        return bad_method()


@app.errorhandler(400)
def bad_msg(error=None):
    message = {
        'status': 400,
        'message': 'msg must exist'
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp


def bad_contentType(error=None):
    message = {
        'status': 400,
        'message': 'Content-Type must be application/json or application/x-www-form-urlencoded'
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp


@app.errorhandler(405)
def bad_method():
    message = {
        'status': 405,
        'message': 'HTTP method must be GET or POST'
    }
    resp = jsonify(message)
    resp.status_code = 405
    return resp


@app.route("/")
def index():
    return render_template("index.html")


import tensorflow as tf
import seq2seq
sess = tf.Session()
sess, model = seq2seq.init_session(sess)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)











