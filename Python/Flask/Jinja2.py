# use Jinja2 
# coding=utf-8
from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/user/<name>')
def user(name):
	# 将name变量传递给Jinja
	return render_template('user.html',name=name)

# 启动服务器
if __name__ =='__main__':
	app.run()