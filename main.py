from flask import Flask, request, abort

app = Flask(__name__) 

from benchmark import *

if __name__ == '__main__':
    app.run(debug=True, port=8000)