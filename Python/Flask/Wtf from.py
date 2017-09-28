# use Jinja2 Bootstrap wtf
# coding=utf-8
from flask_bootstrap import Bootstrap
from flask import Flask,render_template

app=Flask(__name__)
bootstrap=Bootstrap(app)
# 设置wtf秘钥
app.config['SECRET_KEY']='wtf'
# 更改函数，实例化Form表单
# 更改方法，支持Post传值

@app.route('/',methods=['GET','POST'])
def index():
	name =None
	form =NameForm()
	if form.validate_on_submit():
		name= form.name.data
		form.name.data=''
	return render_template('wtfIndex.html',form=form,name=name)
	
@app.route('/user/<name>')
def user(name):
	# 将name变量传递给Jinja	
	return render_template('bootstrapHelloWorld.html',name=name)



from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required

# 新建一个表单，一个text一个submit 可选参数validators是确保提交的字段不为空
class NameForm(Form):
		name= StringField('What is ur name?',validators=[Required()])
		submit = SubmitField('Submit')
# 启动服务器
if __name__ =='__main__':
	app.run()