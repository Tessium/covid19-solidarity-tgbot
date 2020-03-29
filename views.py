from flask import jsonify
from flask import request
import json
from flask import Response
from models import db, Demo


def demo():
    return Response("Cool", 200)