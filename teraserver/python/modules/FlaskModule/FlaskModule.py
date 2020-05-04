from flask import Flask, request, g, url_for
from flask_session import Session
from flask_restx import Api
from libtera.ConfigManager import ConfigManager
from flask_babel import Babel
from modules.BaseModule import BaseModule, ModuleNames
from libtera.db.models.TeraServerSettings import TeraServerSettings

# Flask application
flask_app = Flask("TeraServer")

# Translations
babel = Babel(flask_app)

# API
authorizations = {
    'HTTPAuth': {
        'type': 'basic',
        'in': 'header'
    },
    'Token Authentication': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'default': 'OpenTera',
        'bearerFormat': 'JWT'
    }
}


# Simple fix for API documentation used with reverse proxy
class CustomAPI(Api):
    @property
    def specs_url(self):
        '''
        The Swagger specifications absolute url (ie. `swagger.json`)

        :rtype: str
        '''
        return url_for(self.endpoint('specs'), _external=False)


api = CustomAPI(flask_app, version='1.0.0', title='OpenTeraServer API',
                description='TeraServer API Documentation', doc='/doc', prefix='/api',
                authorizations=authorizations)

# Namespaces
user_api_ns = api.namespace('user', description='API for user calls')
device_api_ns = api.namespace('device', description='API for device calls')
participant_api_ns = api.namespace('participant', description='API for participant calls')
service_api_ns = api.namespace('service', descriptino='API for service calls')


@babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support fr/en in this
    # example.  The best match wins.
    return request.accept_languages.best_match(['fr', 'en'])


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


class FlaskModule(BaseModule):

    def __init__(self,  config: ConfigManager):

        BaseModule.__init__(self, ModuleNames.FLASK_MODULE_NAME.value, config)

        flask_app.debug = True
        # flask_app.secret_key = 'development'
        # Change secret key to use server UUID
        # This is used for session encryption
        flask_app.secret_key = TeraServerSettings.get_server_setting_value(TeraServerSettings.ServerUUID)

        flask_app.config.update({'SESSION_TYPE': 'redis'})
        flask_app.config.update({'BABEL_DEFAULT_LOCALE': 'fr'})
        # TODO set upload folder in config
        # TODO remove this configuration, it is not useful?
        flask_app.config.update({'UPLOAD_FOLDER': 'uploads'})

        # Not sure.
        # flask_app.config.update({'BABEL_DEFAULT_TIMEZONE': 'UTC'})

        self.session = Session(flask_app)

        # Init API
        self.init_user_api()
        self.init_device_api()
        self.init_participant_api()
        self.init_service_api()

        # Init Views
        self.init_views()

    def setup_module_pubsub(self):
        # Additional subscribe
        pass

    def notify_module_messages(self, pattern, channel, message):
        """
        We have received a published message from redis
        """
        print('FlaskModule - Received message ', pattern, channel, message)
        pass

    def init_user_api(self):

        # Default arguments
        kwargs = {'flaskModule': self}

        # Users...
        from .API.user.Login import Login
        from .API.user.Logout import Logout
        from .API.user.QueryUsers import QueryUsers
        from .API.user.QueryForms import QueryForms
        from .API.user.QueryOnlineUsers import QueryOnlineUsers
        from .API.user.QuerySites import QuerySites
        from .API.user.QueryProjects import QueryProjects
        from .API.user.QueryParticipants import QueryParticipants
        from .API.user.QueryDevices import QueryDevices
        from .API.user.QuerySiteAccess import QuerySiteAccess
        from .API.user.QueryDeviceSites import QueryDeviceSites
        from .API.user.QueryDeviceProjects import QueryDeviceProjects
        from .API.user.QueryDeviceParticipants import QueryDeviceParticipants
        from .API.user.QueryProjectAccess import QueryProjectAccess
        from .API.user.QueryParticipantGroup import QueryParticipantGroup
        from .API.user.QuerySessions import QuerySessions
        from .API.user.QuerySessionTypes import QuerySessionTypes
        from .API.user.QuerySessionEvents import QuerySessionEvents
        from .API.user.QueryDeviceData import QueryDeviceData
        from .API.user.QuerySessionTypeDeviceType import QuerySessionTypeDeviceType
        from .API.user.QuerySessionTypeProject import QuerySessionTypeProject
        from .API.user.QueryDeviceSubTypes import QueryDeviceSubTypes
        from .API.user.QueryAssets import QueryAssets
        from .API.user.QueryServices import QueryServices

        # Resources
        user_api_ns.add_resource(Login, '/login', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(Logout, '/logout', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QuerySites, '/sites', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryUsers, '/users', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryForms, '/forms', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryOnlineUsers, '/online', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryProjects, '/projects', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryParticipants, '/participants', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryDevices, '/devices', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryDeviceSites, '/devicesites', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryDeviceProjects, '/deviceprojects', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryDeviceParticipants, '/deviceparticipants', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QuerySiteAccess, '/siteaccess', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryProjectAccess, '/projectaccess', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryParticipantGroup, '/groups', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QuerySessions, '/sessions', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QuerySessionTypes, '/sessiontypes', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QuerySessionTypeDeviceType, '/sessiontypedevicetypes', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QuerySessionTypeProject, '/sessiontypeprojects', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QuerySessionEvents, '/sessionevents', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryDeviceData, '/data', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryDeviceSubTypes, '/devicesubtypes', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryAssets, '/assets', resource_class_kwargs=kwargs)
        user_api_ns.add_resource(QueryServices, '/services', resource_class_kwargs=kwargs)
        api.add_namespace(user_api_ns)

    def init_device_api(self):
        # Default arguments
        kwargs = {'flaskModule': self}

        # Devices
        from .API.device.DeviceLogin import DeviceLogin
        from .API.device.DeviceLogout import DeviceLogout
        from .API.device.DeviceUpload import DeviceUpload
        from .API.device.DeviceRegister import DeviceRegister
        from .API.device.DeviceQuerySessions import DeviceQuerySessions
        from .API.device.DeviceQuerySessionEvents import DeviceQuerySessionEvents
        from .API.device.DeviceQueryDevices import DeviceQueryDevices
        from .API.device.DeviceQueryAssets import DeviceQueryAssets

        # Resources
        # TODO remove legacy endpoint 'device_login'
        device_api_ns.add_resource(DeviceLogin, '/device_login', resource_class_kwargs=kwargs)
        device_api_ns.add_resource(DeviceLogin, '/login', resource_class_kwargs=kwargs)

        # TODO remove legacy endpoint 'device_logout'
        device_api_ns.add_resource(DeviceLogout, '/device_logout', resource_class_kwargs=kwargs)
        device_api_ns.add_resource(DeviceLogout, '/logout', resource_class_kwargs=kwargs)

        # TODO remove legacy endpoint 'device_upload'
        device_api_ns.add_resource(DeviceUpload, '/device_upload', resource_class_kwargs=kwargs)
        device_api_ns.add_resource(DeviceUpload, '/upload', resource_class_kwargs=kwargs)

        # TODO remove legacy endpoint 'device_register'
        device_api_ns.add_resource(DeviceRegister, '/device_register', resource_class_kwargs=kwargs)
        device_api_ns.add_resource(DeviceRegister, '/register', resource_class_kwargs=kwargs)

        device_api_ns.add_resource(DeviceQuerySessions, '/sessions', resource_class_kwargs=kwargs)
        device_api_ns.add_resource(DeviceQuerySessionEvents, '/sessionevents', resource_class_kwargs=kwargs)
        device_api_ns.add_resource(DeviceQueryDevices, '/devices', resource_class_kwargs=kwargs)
        device_api_ns.add_resource(DeviceQueryAssets, '/assets', resource_class_kwargs=kwargs)
        api.add_namespace(device_api_ns)

    def init_participant_api(self):
        # Default arguments
        kwargs = {'flaskModule': self}

        # Participants
        from .API.participant.ParticipantLogin import ParticipantLogin
        from .API.participant.ParticipantLogout import ParticipantLogout
        from .API.participant.ParticipantQueryDeviceData import ParticipantQueryDeviceData
        from .API.participant.ParticipantQueryDevices import ParticipantQueryDevices
        from .API.participant.ParticipantQueryParticipants import ParticipantQueryParticipants
        from .API.participant.ParticipantQuerySessions import ParticipantQuerySessions
        # Resources
        participant_api_ns.add_resource(ParticipantLogin, '/login', resource_class_kwargs=kwargs)
        participant_api_ns.add_resource(ParticipantLogout, '/logout', resource_class_kwargs=kwargs)
        participant_api_ns.add_resource(ParticipantQueryDeviceData, '/data', resource_class_kwargs=kwargs)
        participant_api_ns.add_resource(ParticipantQueryDevices, '/devices', resource_class_kwargs=kwargs)
        participant_api_ns.add_resource(ParticipantQueryParticipants, '/participants', resource_class_kwargs=kwargs)
        participant_api_ns.add_resource(ParticipantQuerySessions, '/sessions', resource_class_kwargs=kwargs)

        api.add_namespace(participant_api_ns)

    def init_service_api(self):
        # Default arguments
        kwargs = {'flaskModule': self}

        # Services
        from .API.service.ServiceQueryParticipants import ServiceQueryParticipants
        service_api_ns.add_resource(ServiceQueryParticipants, '/participants', resource_class_kwargs=kwargs)

        # Add namespace
        api.add_namespace(service_api_ns)

    def init_views(self):
        from .Views.User import User
        from .Views.Upload import Upload
        from .Views.Participant import Participant
        from .Views.DeviceRegistration import DeviceRegistration

        # Default arguments
        args = []
        kwargs = {'flaskModule': self}

        # User test view
        flask_app.add_url_rule('/user', view_func=User.as_view('user', *args, **kwargs))

        # Participant test view
        flask_app.add_url_rule('/participant', view_func=Participant.as_view('participant', *args, **kwargs))

        # flask_app.add_url_rule('/upload/', view_func=Upload.as_view('upload', *args, **kwargs))
        # flask_app.add_url_rule('/device_registration', view_func=DeviceRegistration.as_view('device_register', *args,
        #                                                                                    **kwargs))


@flask_app.after_request
def apply_caching(response):
    # This is required to expose the backend API to rendered webpages from other sources, such as services
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response

