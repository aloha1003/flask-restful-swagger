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
                   description='A Basic Line API')
###################################



def abort_if_todo_doesnt_exist(todo_id):
  if todo_id not in TODOS:
    abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)


@swagger.model
class TodoItem:
  """This is an example of a model class that has parameters in its constructor
  and the fields in the swagger spec are derived from the parameters
  to __init__.
  In this case we would have args, arg2 as required parameters and arg3 as
  optional parameter."""
  def __init__(self, arg1, arg2, arg3='123'):
    pass

class Todo(Resource):
  "My TODO API"
  @swagger.operation(
      notes='get a todo item by ID',
      nickname='get',
      # Parameters can be automatically extracted from URLs (e.g. <string:id>)
      # but you could also override them here, or add other parameters.
      parameters=[
          {
            "name": "todo_id_x",
            "description": "The ID of the TODO item",
            "required": True,
            "allowMultiple": False,
            "dataType": 'string',
            "paramType": "path"
          },
          {
            "name": "a_bool",
            "description": "The ID of the TODO item",
            "required": True,
            "allowMultiple": False,
            "dataType": 'boolean',
            "paramType": "path"
          }
      ])
  def get(self, todo_id):
    # This goes into the summary
    """Get a todo task

    This will be added to the <strong>Implementation Notes</strong>.
    It lets you put very long text in your api.

    Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
    veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
    commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
    velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
    cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
    est laborum.
    """
    abort_if_todo_doesnt_exist(todo_id)
    return TODOS[todo_id], 200, {'Access-Control-Allow-Origin': '*'}

  @swagger.operation(
      notes='delete a todo item by ID',
  )
  def delete(self, todo_id):
    abort_if_todo_doesnt_exist(todo_id)
    del TODOS[todo_id]
    return '', 204, {'Access-Control-Allow-Origin': '*'}

  @swagger.operation(
      notes='edit a todo item by ID',
  )
  def put(self, todo_id):
    args = parser.parse_args()
    task = {'task': args['task']}
    TODOS[todo_id] = task
    return task, 201, {'Access-Control-Allow-Origin': '*'}

  def options (self, **args):
    # since this method is not decorated with @swagger.operation it does not
    # get added to the swagger docs
    return {'Allow' : 'GET,PUT,POST,DELETE' }, 200, \
    { 'Access-Control-Allow-Origin': '*', \
      'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE', \
      'Access-Control-Allow-Headers': 'Content-Type' }

# TodoList
#   shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):

  def get(self):
    return TODOS, 200, {'Access-Control-Allow-Origin': '*'}

  @swagger.operation(
      notes='Creates a new TODO item',
      responseClass=TodoItem.__name__,
      nickname='create',
      parameters=[
          {
            "name": "body",
            "description": "A TODO item",
            "required": True,
            "allowMultiple": False,
            "dataType": TodoItem.__name__,
            "paramType": "body"
          }
      ],
      responseMessages=[
          {
              "code": 201,
              "message": "Created. The URL of the created blueprint should " +
              "be in the Location header"
          },
          {
              "code": 405,
              "message": "Invalid input"
          }
      ])
  def post(self):
    args = parser.parse_args()
    todo_id = 'todo%d' % (len(TODOS) + 1)
    TODOS[todo_id] = {'task': args['task']}
    return TODOS[todo_id], 201, {'Access-Control-Allow-Origin': '*'}

@swagger.model
class ModelWithResourceFields:
  resource_fields = {
      'a_string': fields.String()
  }

@swagger.model
@swagger.nested(
   a_nested_attribute=ModelWithResourceFields.__name__,
   a_list_of_nested_types=ModelWithResourceFields.__name__)
class TodoItemWithResourceFields:
  """This is an example of how Output Fields work
  (http://flask-restful.readthedocs.org/en/latest/fields.html).
  Output Fields lets you add resource_fields to your model in which you specify
  the output of the model when it gets sent as an HTTP response.
  flask-restful-swagger takes advantage of this to specify the fields in
  the model"""
  resource_fields = {
      'a_string': fields.String(attribute='a_string_field_name'),
      'a_formatted_string': fields.FormattedString,
      'an_enum': fields.String,
      'an_int': fields.Integer,
      'a_bool': fields.Boolean,
      'a_url': fields.Url,
      'a_float': fields.Float,
      'an_float_with_arbitrary_precision': fields.Arbitrary,
      'a_fixed_point_decimal': fields.Fixed,
      'a_datetime': fields.DateTime,
      'a_list_of_strings': fields.List(fields.String),
      'a_nested_attribute': fields.Nested(ModelWithResourceFields.resource_fields),
      'a_list_of_nested_types': fields.List(fields.Nested(ModelWithResourceFields.resource_fields)),
  }

  # Specify which of the resource fields are required
  required = ['a_string']

  swagger_metadata = {
      'an_enum': {
          'enum': ['one', 'two', 'three']
      }
  }

class MarshalWithExample(Resource):
  @swagger.operation(
      notes='get something',
      responseClass=TodoItemWithResourceFields,
      nickname='get')
  @marshal_with(TodoItemWithResourceFields.resource_fields)
  def get(self, **kwargs):
    return {}, 200,  {'Access-Control-Allow-Origin': '*'}

# # The socket.io namespace
# class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
#     def on_nickname(self, nickname):
#         self.environ.setdefault('nicknames', []).append(nickname)
#         self.socket.session['nickname'] = nickname
#         self.broadcast_event('announcement', '%s has connected' % nickname)
#         self.broadcast_event('nicknames', self.environ['nicknames'])
#         # Just have them join a default-named room
#         self.join('main_room')

#     def on_user_message(self, msg):
#         self.emit_to_room('main_room', 'msg_to_room', self.socket.session['nickname'], msg)

#     def recv_message(self, message):
#         print "PING!!!", message

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<string:todo_id>')
api.add_resource(MarshalWithExample, '/marshal_with')

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
        # print self.id
        # print self.password
        # print keyname
        # print self.ip
        
        

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
            yield 'Your Token is <br>'+ msg.authToken
        elif msg.type == 2:
            msg = "require QR code"
            self.raise_error(msg)
        else:
            msg = "require device confirm"
            self.raise_error(msg)
        # client = LineClient(account, password)
         
    return Response(lineLogin(request.form), mimetype='text/html')

# @app.route('/login')
# def login():
#     return render_template('chat.html')

# @app.route("/socket.io/<path:path>")
# def run_socketio(path):
#     socketio_manage(request.environ, {'': ChatNamespace})



if __name__ == '__main__':
    app.run(debug=True)
    
  
  
