from flask import jsonify, session
from flask_restplus import Resource, reqparse, fields
from modules.LoginModule.LoginModule import http_auth
from modules.FlaskModule.FlaskModule import user_api_ns as api


model = api.model('Login', {
    'websocket_url': fields.String,
    'user_uuid': fields.String,
    'user_token': fields.String
})


class Login(Resource):

    def __init__(self, _api, *args, **kwargs):
        Resource.__init__(self, _api, *args, **kwargs)
        self.module = kwargs.get('flaskModule', None)
        self.parser = reqparse.RequestParser()

    @http_auth.login_required
    @api.doc(description='Login to the server using HTTP Basic Authentification (HTTPAuth)')
    @api.marshal_with(model, mask=None)
    def get(self):

        session.permanent = True

        # Redis key is handled in LoginModule
        servername = self.module.config.server_config['hostname']
        port = self.module.config.server_config['port']

        # Get user token key from redis
        from modules.Globals import TeraServerConstants
        token_key = self.module.redisGet(TeraServerConstants.RedisVar_UserTokenAPIKey)

        # Get token for user
        from libtera.db.models.TeraUser import TeraUser
        user_token = TeraUser.get_token_for_user(session['_user_id'], token_key)

        # Return reply as json object
        reply = {"websocket_url": "wss://" + servername + ":" + str(port) + "/wss?id=" + session['_id'],
                 "user_uuid": session['_user_id'],
                 "user_token": user_token}

        return reply
