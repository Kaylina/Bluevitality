## flask quick start
## http://docs.jinkan.org/docs/flask/quickstart.html#quickstart

from flask import Flask
app = Flask(__name__)

## about this `Decorator`, see: http://www.cnblogs.com/Jerry-Chou/archive/2012/05/23/python-decorator-explain.html
@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/hello')
def hello_world():
    return 'Hi there!'

@app.route('/index')
def index():
    return 'Index Page'

## parameter
@app.route('/user/<username>')
def show_user_profile(username):
    return 'User profile \n Name: %s' % username

## specific type parameter
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id

## '/' redirection
## 'projects' will be redirected to 'projects/'
@app.route('/projects/')
def projects():
    return 'The project page'

## 'about/' will generate 404 error
@app.route('/about')
def about():
    return 'About'

if __name__ == '__main__':
    app.run(debug=True)