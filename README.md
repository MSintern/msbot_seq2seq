# 基于Tensorflow seq2seq实现对答机器人
本项目利用Tensorflow seq2seq模型，实现了简单的闲聊式对答机器人；并使用Flask，实现了机器人的web端展示。

## 环境：
* 本地环境： ubuntu 16.04+python 3.6
* 服务器环境： CentOS 7.3+python 3.5

建议用 Anaconda 4.4.0 python 3.6 verson 安装python3 和 Tensorflow 等。
 
## 参考开源项目：
* Tensorflow官方translate模型：https://github.com/tensorflow/models/tree/master/tutorials/rnn/translate
* 使用TensorFlow实现的Sequence to Sequence的聊天机器人模型：https://github.com/qhduan/Seq2Seq_Chatbot_QA
* easybot：https://github.com/undersail/easybot
* dgk_lost_conv 中文对白语料：https://github.com/majoressense/dgk_lost_conv

## 后记：
我是在本地端训练模型，然后将模型部署在了阿里云，大家可以通过101.200.59.7进行访问。有关阿里云的部署我在[博客](http://houjiateng.com/2017/08/21/Tensorflow+Flask+Nginx+Gunicorn%E5%9C%A8%E9%98%BF%E9%87%8C%E4%BA%91%E7%9A%84%E9%83%A8%E7%BD%B2/)上有比较详细的说明，有关api的调用方式也可以查阅我的[博客](http://houjiateng.com/2017/08/22/%E4%BD%BF%E7%94%A8Flask%E4%B8%BA%E5%AF%B9%E7%AD%94%E6%9C%BA%E5%99%A8%E4%BA%BA%E5%86%99%E4%B8%AARESTful%20API%20/)。



