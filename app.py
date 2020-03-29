from flask import Flask
from views import demo


app = Flask(__name__)

app.add_url_rule('/demo',  methods=['POST', 'GET'], view_func=demo)
