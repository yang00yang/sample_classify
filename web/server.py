#-*- coding:utf-8 -*-
from flask import Flask,jsonify,request,render_template
import base64,cv2,numpy as np,logging
from threading import current_thread
import os,sys
from main import sample
from main import check
import json
app = Flask(__name__,root_path="web")
person_img_num = 2000

logger = logging.getLogger("WebServer")

@app.route("/")
def index():
    return render_template('index.html',version="version")


def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return str(img_stream,'utf-8')

# 开始任务
@app.route('/start',methods=['GET'])
def start():
    username = request.args['username']
    if check.get_status(username) == 0:
        # 没有领任务
        sample.get_img_by_person(person_img_num,username)

    # 已经有任务
    img_path,label = check.get_img_in_src(username)
    if img_path == '' or label == '':
        return ''
    img_stream = return_img_stream(img_path)
    return jsonify({'img_stream': str(img_stream),'img_path':img_path,'label':label})

# 图片判定
@app.route('/check',methods=['POST'])
def img_check():
    username = request.json.get('username')
    type = request.json.get('type')
    img_path = request.json.get('img_path')
    check.move_img_good_or_bad(username,type,img_path)
    return "ok"


if __name__ == '__main__':
    app.run(debug=True, port=8082)