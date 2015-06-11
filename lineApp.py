#-*- coding: utf-8 -*-
'''
Running:

  PYTHONPATH=. python examples/lineApp.py

'''

from flask import Flask
from line_login import line_login
from lineapi import lineapi


app = Flask(__name__)

if __name__ == '__main__':
  
  app.register_blueprint(line_login)
  app.register_blueprint(lineapi)
  app.run(debug=True)



