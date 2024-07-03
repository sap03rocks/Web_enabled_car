import flask
from flask import Flask, render_template
from flask import request
import flask_login
import requests
from flask_cors import CORS


# Example user data (replace with your actual user data)
users = {
    'admin': {'password': 'admin'}
}


app = flask.Flask(__name__)
app.secret_key = 'hellofriends'
CORS(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')
               

    email = flask.request.form['email']
    if email in users and flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('home'))

    return render_template('incorrectpassword.html')



@app.route('/home')
@flask_login.login_required
def home():
    return render_template('index.html')

@app.route('/logout' ,methods=['GET'])
def logout():
    flask_login.logout_user()
    return render_template('logout.html')


@app.route('/location', methods=['POST','GET'])
def location():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    token = ""
    chat_id = ""
    method="sendMessage"
    text="the location of the car is latitude={0} and longitude={1}".format(latitude,longitude)

    response = requests.post(
        url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
        data={'chat_id': chat_id , 'text': text}
    ).json()
    print(response)
    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
