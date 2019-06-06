from flask import jsonify, session, request
from flask_restful import Resource, reqparse
from modules.Globals import auth
from libtera.db.models.TeraUser import TeraUser
from libtera.db.models.TeraSession import TeraSession
from libtera.db.DBManager import DBManager
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import exc


class QuerySessionTypes(Resource):

    def __init__(self, flaskModule=None):
        Resource.__init__(self)
        self.module = flaskModule

    @auth.login_required
    def get(self):
        current_user = TeraUser.get_user_by_uuid(session['user_id'])
        user_access = DBManager.userAccess(current_user)

        parser = reqparse.RequestParser()
        parser.add_argument('id_session_type', type=int, help='id_session')
        parser.add_argument('list', type=bool)

        args = parser.parse_args()

        session_types = []

        if args['id_session_type']:
            session_types = [user_access.query_session_type_by_id(args['id_session_type'])]
        else:
            session_types = user_access.get_accessible_session_types()

        try:
            sessions_types_list = []
            for st in session_types:
                if args['list'] is None:
                    st_json = st.to_json()
                    sessions_types_list.append(st_json)
                else:
                    st_json = st.to_json(minimal=True)
                    sessions_types_list.append(st_json)

            return jsonify(sessions_types_list)

        except InvalidRequestError:
            return '', 500

    @auth.login_required
    def post(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('participant', type=str, location='json', help='Partiicpant to create / update',
        #                     required=True)
        #
        # current_user = TeraUser.get_user_by_uuid(session['user_id'])
        # user_access = DBManager.userAccess(current_user)
        # # Using request.json instead of parser, since parser messes up the json!
        # if 'participant' not in request.json:
        #     return '', 400
        #
        # json_participant = request.json['participant']
        #
        # # Validate if we have an id
        # if 'id_participant' not in json_participant or 'id_participant_group' not in json_participant:
        #     return '', 400
        #
        # # Check if current user can modify the posted group
        # # User can modify or add a group if it has admin access to that project
        # if json_participant['id_participant_group'] not in user_access.get_accessible_groups_ids(admin_only=True):
        #     return '', 403
        #
        # # Do the update!
        # if json_participant['id_participant'] > 0:
        #     # Already existing
        #     try:
        #         TeraParticipant.update_participant(json_participant['id_participant'], json_participant)
        #     except exc.SQLAlchemyError:
        #         import sys
        #         print(sys.exc_info())
        #         return '', 500
        # else:
        #     # New
        #     try:
        #         new_part = TeraParticipant()
        #         new_part.from_json(json_participant)
        #         TeraParticipant.insert_participant(new_part)
        #         # Update ID for further use
        #         json_participant['id_participant'] = new_part.id_participant
        #     except exc.SQLAlchemyError:
        #         import sys
        #         print(sys.exc_info())
        #         return '', 500
        #
        # # TODO: Publish update to everyone who is subscribed to sites update...
        # update_participant = TeraParticipant.get_participant_by_id(json_participant['id_participant'])
        #
        # return jsonify([update_participant.to_json()])
        return '', 501

    @auth.login_required
    def delete(self):
        return '', 501
