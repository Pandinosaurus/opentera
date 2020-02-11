from flask import jsonify, session
from flask_restplus import Resource, reqparse
from modules.LoginModule.LoginModule import multi_auth
from modules.FlaskModule.FlaskModule import user_api_ns as api
from sqlalchemy.exc import InvalidRequestError
from libtera.db.models.TeraUser import TeraUser
from libtera.redis.AsyncRedisSubscribeWait import AsyncRedisSubscribeWait
from modules.BaseModule import ModuleNames
from messages.python.RPCMessage_pb2 import RPCMessage, Value
import datetime


class QueryOnlineUsers(Resource):
    def __init__(self, _api, *args, **kwargs):
        Resource.__init__(self, _api, *args, **kwargs)
        self.flaskModule = kwargs.get('flaskModule', None)
        self.parser = reqparse.RequestParser()

    @multi_auth.login_required
    @api.doc(description='Get online users. CURRENTLY UNIMPLEMENTED.',
             responses={200: 'Success'})
    def get(self):
        current_user = TeraUser.get_user_by_uuid(session['_user_id'])
        args = self.parser.parse_args()

        my_args = {}

        try:

            # This needs to be an unique name
            my_name = 'module.' + self.flaskModule.module_name + '.OnlineUsers.' + session['_user_id']

            req = AsyncRedisSubscribeWait(my_name, self.flaskModule)
            req.listen()

            # Publish request
            message = RPCMessage()
            message.method = 'online_users'
            message.timestamp = datetime.datetime.now().timestamp()
            message.id = 1
            message.reply_to = my_name

            self.flaskModule.publish('module.' + ModuleNames.USER_MANAGER_MODULE_NAME.value + '.rpc',
                                     message.SerializeToString())

            # Wait for answer, no timeout
            (pattern, channel, data) = req.wait()

            req.stop()

            print('event received', pattern, channel, data)

            return jsonify(data)
        except InvalidRequestError:
            return '', 500

    # def post(self):
    #     return '', 501
    #
    # def delete(self):
    #     return '', 501

