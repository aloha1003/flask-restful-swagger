#-*- coding: utf-8 -*-
'''
Running:

  PYTHONPATH=. python examples/lineApp.py

'''

from flask import Flask

from flask import Blueprint

line_login = Blueprint('line_login', __name__)



from flask import Flask, redirect, request, render_template
from flask.ext.restful import reqparse, abort, Api, Resource, fields,\
    marshal_with
from flask_restful_swagger import swagger 
from flask import Response


from line import LineClient, LineGroup, LineContact

# Line Lib                    #
import rsa
import requests
try:
    import simplejson as json
except ImportError:
    import json

from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol
import sys
reload(sys)

sys.setdefaultencoding("utf-8")

#from curve import CurveThrift
from curve import CurveThrift
from curve.ttypes import TalkException
from curve.ttypes import ToType, ContentType,OperationType, Provider

# Line lib end                    #

app = Flask(__name__, static_folder='../static')



class lineDemo():
    def __init__(self, data):
        self.session = requests.session()
        self._headers = {}
        self.id=data['account']
        self.password=data['password']
        self.LINE_DOMAIN = "http://gd2.line.naver.jp"
        self.LINE_SESSION_LINE_URL  = self.LINE_DOMAIN + "/authct/v1/keys/line"
        self.LINE_HTTP_URL          = self.LINE_DOMAIN + "/api/v4/TalkService.do"
        self.LINE_CERTIFICATE_URL   = self.LINE_DOMAIN + "/Q"
        self.com_name = 'carpedm20'
        self.ip       = "127.0.0.1"
        self.provider = CurveThrift.Provider.LINE # LINE
        self.provider = Provider.LINE # LINE
        self.version     = "3.7.0"
        
        self.revision    = 0
        os_version = "10.9.4-MAVERICKS-x64"
        user_agent = "DESKTOP:MAC:%s(%s)" % (os_version, self.version)
        app = "DESKTOPMAC\t%s\tMAC\t%s" % (self.version, os_version)
        self._headers['User-Agent']         = user_agent
        self._headers['X-Line-Application'] = app
    def get_json(self, url):
        """Get josn from given url with saved session and headers"""
        return json.loads(self.session.get(url, headers=self._headers).text)


@line_login.route('/login')
def login():
    return render_template('login.html')
@line_login.route('/loginProcess', methods=['POST'])
def loginProcess():
    def lineLogin(data):
        
        self = lineDemo(data)

        """Login to LINE server."""
        

        j = self.get_json(self.LINE_SESSION_LINE_URL)
        

        session_key = j['session_key']
        message     = (chr(len(session_key)) + session_key +
                       chr(len(self.id)) + self.id +
                       chr(len(self.password)) + self.password).encode('utf-8')

        keyname, n, e = j['rsa_key'].split(",")
        pub_key       = rsa.PublicKey(int(n,16), int(e,16))
        crypto        = rsa.encrypt(message, pub_key).encode('hex')

        self.transport = THttpClient.THttpClient(self.LINE_HTTP_URL)
        self.transport.setCustomHeaders(self._headers)

        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self._client   = CurveThrift.Client(self.protocol)
      
        msg = self._client.loginWithIdentityCredentialForCertificate(
                self.id, self.password, keyname, crypto, False, self.ip,
                self.com_name, self.provider, "")
        
        self._headers['X-Line-Access'] = msg.verifier
        self._pinCode = msg.pinCode
        message = "Enter PinCode '%s' to your mobile phone in 2 minutes"\
                % self._pinCode
        yield message
        print message
        

        j = self.get_json(self.LINE_CERTIFICATE_URL)

        self.verifier = j['result']['verifier']

        msg = self._client.loginWithVerifierForCertificate(self.verifier)

        if msg.type == 1:
            self.certificate = msg.certificate
            self.authToken = self._headers['X-Line-Access'] = msg.authToken
            yield '<br> Your Token is <br> <textarea readonly="readonly" cols="20" rows="5">'+ msg.authToken+'</textarea>'
        elif msg.type == 2:
            msg = "require QR code"
            self.raise_error(msg)
        else:
            msg = "require device confirm"
            self.raise_error(msg)
        return
    return Response(lineLogin(request.form), mimetype='text/html')



