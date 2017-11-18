from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify, make_response, Response
from sqlalchemy.sql.functions import func
from functools import wraps
import json
import CustomFlask from assets.custom

app = CustomFlask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets/users.db'
db.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('listStudents.html')


app.run(host='0.0.0.0', port=8080, debug=True)
