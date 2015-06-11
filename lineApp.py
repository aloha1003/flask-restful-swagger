#-*- coding: utf-8 -*-
'''
Running:

  PYTHONPATH=. python examples/lineApp.py

'''


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

###################################
# This is important:
api = swagger.docs(Api(app), apiVersion='0.1',
                   basePath='http://localhost:5000',
                   resourcePath='/',
                   produces=["application/json", "text/html"],
                   api_spec_url='/api/spec',
                   description='Line API')
###################################



def abort_if_todo_doesnt_exist(todo_id):
  if todo_id not in TODOS:
    abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()

parser.add_argument('token', type=str, location='headers')

class LineContactParse:
    def parse(self,raw_contact):
        contacts = []
        for contact in raw_contact:
            obj ={}
            obj['id'] = contact.id
            obj['name'] = contact.name
            obj['statusMessage'] = contact.statusMessage
            contacts.append(obj)
        return json.dumps(contacts)
class LineGroupParse:
    def parse(self,raw_groups):
        if type(raw_groups is list) :
            groups = []

            for group in raw_groups:
                tmp = json.loads(str(group))
                groups.append(tmp)
            return json.dumps(groups)
        else:
            return json.dumps(json.loads(str(raw_groups)))
class LineTokenChecker:
    msg = None

    def check(self,client):
        "因為上面是建構元，不能回傳任何錯誤，所以另外寫一隻checkAuth去測試Token"
        checkAuth = client.checkAuth()
        # "因為上面是建構元，不能回傳任何錯誤，所以另外寫一隻checkAuth去測試Token"
        # checkAuth = client.checkAuth()
        # try :
        #     if (checkAuth["message"]):
        #        return json.loads(lineTokenChecker.msg),505,{'Access-Control-Allow-Origin': '*'}
        # except:
        try :
            self.msg = str(json.dumps(checkAuth))
            return False;
        except:
            return True;
class Profile(Resource):
    "Profile"
    @swagger.operation(
        notes='取得個人資料',
        nickname='getProfile',
        parameters=[
            {
             "name": "token",
             "description": "Line 登入Token",
             "required": True,
             "dataType": 'string',
             "paramType": "header"
            }
        ],
        responseMessages=[
        {
           "code": 200,
           "message": "Created. The URL of the created blueprint should " +
           "be in the Location header"
          },
          {
              "code": 505,
              "message": "Please Input valid Token"
          }
        ])
    def get(self):
        args = parser.parse_args()
        token = args['token']
        client = LineClient(authToken=token)
        lineTokenChecker = LineTokenChecker()
        if (lineTokenChecker.check(client)) :
            profile = str(client.getProfile())
            return json.loads(profile), 200, {'Access-Control-Allow-Origin': '*'}
        else :
            return json.loads(lineTokenChecker.msg),505,{'Access-Control-Allow-Origin': '*'}
class Contacts(Resource):
    "Contacts"
    @swagger.operation(
        notes='取得聯絡人',
        nickname='getProfile',
        parameters=[
            {
             "name": "token",
             "description": "Line Login Token",
             "required": True,
             "dataType": 'string',
             "paramType": "header"
            }
        ],
        responseMessages=[
          {
           "code": 200,
           "message": "Created. The URL of the created blueprint should " +
           "be in the Location header"
          },
          {
              "code": 505,
              "message": "Please Input valid Token"
          }
        ]
    )
    def get(self):
        args = parser.parse_args()
        token = args['token']
        client = LineClient(authToken=token)
        lineTokenChecker = LineTokenChecker()
        if (lineTokenChecker.check(client)) :
            lineContactParse = LineContactParse()
            contacts = lineContactParse.parse(client.contacts)
            return json.loads(contacts), 200, {'Access-Control-Allow-Origin': '*'}
        else :
            return json.loads(lineTokenChecker.msg),505,{'Access-Control-Allow-Origin': '*'}
    @swagger.operation(
        notes='更新聯絡人列表',
        nickname='search',
        parameters=[
            {
             "name": "token",
             "description": "Line Login Token",
             "required": True,
             "dataType": 'string',
             "paramType": "header"
            }
        ],
        responseMessages=[
          {
           "code": 200,
           "message": "Created. The URL of the created blueprint should " +
           "be in the Location header"
          },
          {
              "code": 505,
              "message": "Please Input valid Token"
          }
        ]
    )
    def put(self):
        args = parser.parse_args()
        token = args['token']
        client = LineClient(authToken=token)
        lineTokenChecker = LineTokenChecker()
        if (lineTokenChecker.check(client)) :
            lineContactParse = LineContactParse()
            contacts = lineContactParse.parse(client.contacts)
            return json.loads(contacts), 200, {'Access-Control-Allow-Origin': '*'}
        else :
            return json.loads(lineTokenChecker.msg),505,{'Access-Control-Allow-Origin': '*'}
class Contacts_Search(Resource):
    "Contacts"
    @swagger.operation(
        notes='透過Id尋找好友',
        nickname='search',
        parameters=[
            {
             "name": "token",
             "description": "Line Login Token",
             "required": True,
             "dataType": 'string',
             "paramType": "header"
            },
            {
             "name": "id",
             "description": "Line 聯絡人Id",
             "required": False,
             "dataType": 'string',
             "paramType": "query"
            },
            {
             "name": "name",
             "description": "Line 聯絡人姓名",
             "required": False,
             "dataType": 'string',
             "paramType": "query"
            }
        ],
        responseMessages=[
          {
           "code": 200,
           "message": "Created. The URL of the created blueprint should " +
           "be in the Location header"
          },
          {
              "code": 505,
              "message": "Please Input valid Token"
          }
        ]
    )
    def get(self):
        parser.add_argument('id', type=str, location='args')
        parser.add_argument('name', type=str, location='args')
        args = parser.parse_args()
        token = args['token']
        try:
            id = args['id']
        except IndexError :
            id = False
        try:
            name = args['name']
        except IndexError :
            name = False
        client = LineClient(authToken=token)
        lineTokenChecker = LineTokenChecker()
        if (lineTokenChecker.check(client)) :
            if (id) :
                profile = str(client.getContactById(id))
            elif (name) :
                profile = str(client.getContactByName(name))
            else:
                lineContactParse = LineContactParse()
                profile = lineContactParse.parse(client.contacts)
            return json.loads(profile), 200, {'Access-Control-Allow-Origin': '*'}

        else :
            return json.loads(lineTokenChecker.msg),505,{'Access-Control-Allow-Origin': '*'}

class Message(Resource):
    "message"
    @swagger.operation(
        notes='取得訊息',
        nickname='sendMessage',
        parameters=[
            {
             "name": "token",
             "description": "Line Login Token",
             "required": True,
             "dataType": 'string',
             "paramType": "header"
            },
            {
             "name": "id",
             "description": "Line 聯絡人Id 或是 群組 id 或是 聊天室 id",
             "required": True,
             "dataType": 'string',
             "paramType": "query"
            }
        ],
        responseMessages=[
          {
           "code": 200,
           "message": "Created. The URL of the created blueprint should " +
           "be in the Location header"
          },
          {
              "code": 505,
              "message": "Please Input valid Token"
          },
          {
              "code": 506,
              "message": "Please Input Id"
          }
        ]
    )
    def get(self):
        parser.add_argument('id', type=str, location='args')
        args = parser.parse_args()
        token = args['token']
        try:
            id = args['id']
        except IndexError :
            return {} , 506, {'Access-Control-Allow-Origin': '*'}
        client = LineClient(authToken=token)
        lineTokenChecker = LineTokenChecker()
        if (lineTokenChecker.check(client)) :
            try :
                if (id[0] =='u'):
                    contact = client.getContactById(id)
                    if contact :
                        message = client.getMessageBox(id)
                        msg ={}
                        msg["status"] = message.status
                        msg["unreadCount"] = message.unreadCount
                        msg["lastSeq"] = message.lastSeq
                        lastMessages = {} 
                        msg["lastMessages"]= (message.lastMessages[0].__dict__)

                        msg["midType"] = message.midType
                        msg["channelId"] = message.channelId, 
                        msg["lastModifiedTime"] = message.lastModifiedTime  
                        msg["id"] = message.id
                        return msg, 200, {'Access-Control-Allow-Origin': '*'}
                    else :
                        return {'status':'failure','msg':'找不到使用者'}, 500, {'Access-Control-Allow-Origin': '*'}
                elif (id[0] =='c'):
                    group = client.getGroupById(id)
                    if group :
                        message = client.getMessageBox(id)
                        msg ={}
                        msg["status"] = message.status
                        msg["unreadCount"] = message.unreadCount
                        msg["lastSeq"] = message.lastSeq
                        lastMessages = {} 
                        msg["lastMessages"]= (message.lastMessages[0].__dict__)

                        msg["midType"] = message.midType
                        msg["channelId"] = message.channelId, 
                        msg["lastModifiedTime"] = message.lastModifiedTime  
                        msg["id"] = message.id
                        return msg, 200, {'Access-Control-Allow-Origin': '*'}
                    else :
                        return {'status':'failure','msg':'找不到使用者'}, 500, {'Access-Control-Allow-Origin': '*'}
                else :
                    return {'status':'failure','msg':'錯誤的id'}, 500, {'Access-Control-Allow-Origin': '*'}
            except Exception :
                print Exception
            return {'status':'failure'}, 500, {'Access-Control-Allow-Origin': '*'}
        else :
            return json.loads(lineTokenChecker.msg),505,{'Access-Control-Allow-Origin': '*'}
class SendMessage(Resource):
    "SendMessage"
    @swagger.operation(
        notes='傳送訊息',
        nickname='sendMessage',
        parameters=[
            {
             "name": "token",
             "description": "Line Login Token",
             "required": True,
             "dataType": 'string',
             "paramType": "header"
            },
            {
             "name": "id",
             "description": "Line 聯絡人Id 或是 群組 id 或是 聊天室 id",
             "required": True,
             "dataType": 'string',
             "paramType": "form"
            },
            {
             "name": "message",
             "description": "訊息內容",
             "required": True,
             "dataType": 'string',
             "paramType": "form"
            }

        ],
        responseMessages=[
          {
           "code": 200,
           "message": "Created. The URL of the created blueprint should " +
           "be in the Location header"
          },
          {
              "code": 505,
              "message": "Please Input valid Token"
          },
          {
              "code": 506,
              "message": "Please Input Id"
          }
        ]
    )
    def post(self):
        parser.add_argument('id', type=str, location='form')
        parser.add_argument('message', type=str, location='form')
        args = parser.parse_args()
        token = args['token']
        try:
            id = args['id']
        except IndexError :
            return {"message": "沒有傳入Id"} , 506, {'Access-Control-Allow-Origin': '*'}
        try:
            message = args['message']
        except IndexError :
            return {"message": "message"} , 506, {'Access-Control-Allow-Origin': '*'}
        client = LineClient(authToken=token)
        lineTokenChecker = LineTokenChecker()
        if (lineTokenChecker.check(client)) :
            try :
                if (id[0] =='u'):
                    contact = client.getContactById(id)
                    if contact :
                        res = contact.sendMessage(message)
                        return {'status':'success'}, 200, {'Access-Control-Allow-Origin': '*'}
                    else :
                        return {'status':'failure','msg':'找不到使用者'}, 500, {'Access-Control-Allow-Origin': '*'}
                elif (id[0] =='c'):
                    group = client.getGroupById(id)
                    if group :
                        res = group.sendMessage(message)
                        return {'status':'success'}, 200, {'Access-Control-Allow-Origin': '*'}
                    else :
                        return {'status':'failure','msg':'找不到群組'}, 500, {'Access-Control-Allow-Origin': '*'}
                else:
                    return {'status':'failure','msg':'錯誤的Id'}, 500, {'Access-Control-Allow-Origin': '*'}

            except Exception :
               print Exception
            return {'status':'failure'}, 500, {'Access-Control-Allow-Origin': '*'}
        else :
            return json.loads(lineTokenChecker.msg),505,{'Access-Control-Allow-Origin': '*'}


class Groups(Resource):
    @swagger.operation(
        notes='取得聊天室群組',
        nickname='getGroups',
        parameters=[
            {
             "name": "token",
             "description": "Line Login Token",
             "required": True,
             "dataType": 'string',
             "paramType": "header"
            }
        ],
        responseMessages=[
          {
           "code": 200,
           "message": "Created. The URL of the created blueprint should " +
           "be in the Location header"
          },
          {
              "code": 505,
              "message": "Please Input valid Token"
          },
          {
              "code": 506,
              "message": "Please Input Id"
          }
        ]
    )
    def get(self):
        args = parser.parse_args()
        token = args['token']
        client = LineClient(authToken=token)
        lineTokenChecker = LineTokenChecker()
        if (lineTokenChecker.check(client)) :
            lineGroupParse = LineGroupParse()
            groups = lineGroupParse.parse(client.groups)
            return json.loads(groups), 200, {'Access-Control-Allow-Origin': '*'}
        else :
            return json.loads(lineTokenChecker.msg),505,{'Access-Control-Allow-Origin': '*'}
class Groups_Search(Resource):
    @swagger.operation(
        notes='搜尋群組',
        nickname='getGroups',
        parameters=[
            {
             "name": "token",
             "description": "Line Login Token",
             "required": True,
             "dataType": 'string',
             "paramType": "header"
            },
            {
             "name": "id",
             "description": "群組 id",
             "required": False,
             "dataType": 'string',
             "paramType": "query"
            },
            {
             "name": "name",
             "description": "Line 聊天室",
             "required": False,
             "dataType": 'string',
             "paramType": "query"
            }
        ],
        responseMessages=[
          {
           "code": 200,
           "message": "Created. The URL of the created blueprint should " +
           "be in the Location header"
          },
          {
              "code": 505,
              "message": "Please Input valid Token"
          },
          {
              "code": 506,
              "message": "Please Input Id"
          }
        ]
    )
    def get(self):
        parser.add_argument('id', type=str, location='args')
        parser.add_argument('name', type=str, location='args')
        args = parser.parse_args()
        token = args['token']
        try:
            id = args['id']
        except IndexError :
            id = False
        try:
            name = args['name']
        except IndexError :
            name = False
        args = parser.parse_args()
        token = args['token']
        client = LineClient(authToken=token)
        lineTokenChecker = LineTokenChecker()
        if (lineTokenChecker.check(client)) :
            if (id) :
                groups = client.getGroupById(id)
                groups = json.dumps(json.loads(str(groups)))
            elif (name) :
                groups = client.getGroupByName(name)
                groups = json.dumps(json.loads(str(groups)))
            else:
                groups = client.groups
                lineGroupParse = LineGroupParse()
                groups = lineGroupParse.parse(groups)
            return json.loads(groups), 200, {'Access-Control-Allow-Origin': '*'}
        else :
            return json.loads(lineTokenChecker.msg),505,{'Access-Control-Allow-Origin': '*'}


api.add_resource(Profile, '/profile')
api.add_resource(Contacts, '/contacts')
api.add_resource(Contacts_Search, '/contacts/search')
api.add_resource(Groups, '/groups')
api.add_resource(Groups_Search, '/groups/search')
api.add_resource(Message, '/message')
api.add_resource(SendMessage, '/message/send')


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

@app.route('/docs')
def docs():
  return redirect('/static/docs.html')

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/loginProcess', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)

