from flask import Flask, url_for, request

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print 'POST'
    else:
        print 'GET'
    return 'You are so stupid.'

with app.test_request_context():
    print url_for('login')
    print url_for('login', method='POST')

if __name__ == '__main__':
    app.run(debug=True)