#-*- coding: utf-8 -*-
'''
Running:

  PYTHONPATH=. python examples/lineApp.py

'''

from flask import Flask

from flask import Blueprint

lineapi = Blueprint('lineapi', __name__, static_folder='../static')



from flask import Flask, redirect, request, render_template
from flask.ext.restful import reqparse, abort, Api, Resource, fields,\
    marshal_with
from flask_restful_swagger import swagger 
from flask import Response


from line import LineClient, LineGroup, LineContact




###################################
# This is important:
api = swagger.docs(Api(lineapi), apiVersion='0.1',
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


@lineapi.route('/docs')
def docs():
  return redirect('/static/docs.html')


