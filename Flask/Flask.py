#coding=utf-8

from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])           #判断使用的HTTP方法
def login():
    if request.method == 'GET':
        return 'Use Get'
    else:
        return 'Use Post'

@app.route('/upload/<path>', methods=['GET', 'POST'])   #将URL后的路径以变量形式传递给参数
def upload(path):                                       #接收参数path
    if request.method == 'GET':
        if os.path.isdir(os.getcwd()+"\\"+path):        #判断当前文件夹下有无URL中变量指定的文件夹,否则报错
            return render_template("upload.html",up_path=path)  #返回渲染后的模板（传递给模板的变量为up_path,模板文件内引用的形式为：{{up_path}}）
        else:
            return '输入的路径不存在...'
    elif request.method == 'POST':
        UPLOAD_FOLDER = path                            #指定存放的资源位置（URL中uploads路径后指定的文件夹名称）
        f = request.files['file']                       #获取文件流
        file_name = secure_filename(f.filename)         #安全的获取文件名
        f.save(os.path.join(UPLOAD_FOLDER, file_name))  #将上传的资源存放至指定路径下
        return '上传成功'

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
