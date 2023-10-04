from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from .orm import getDespesas_ano

app = Flask(__name__)
CORS(app)


@app.route('/despesas/<ano>', methods=['GET'])
@cross_origin(origins=['http://localhost:8080'])
def dados(ano):
    
