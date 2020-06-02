from flask import jsonify, session, request
from flask_restx import Resource, reqparse, inputs
from sqlalchemy import exc
from modules.LoginModule.LoginModule import user_multi_auth
from modules.FlaskModule.FlaskModule import user_api_ns as api
from libtera.db.models.TeraUser import TeraUser
from libtera.db.models.TeraSiteAccess import TeraSiteAccess
from modules.DatabaseModule.DBManager import DBManager

# Parser definition(s)
get_parser = api.parser()
get_parser.add_argument('id_user', type=int, help='ID of the user from which to request all site roles')
get_parser.add_argument('id_user_group', type=int, help='ID of the user group from which to request all site roles')
get_parser.add_argument('id_site', type=int, help='ID of the site from which to request all user groups roles')
get_parser.add_argument('admins', type=inputs.boolean, help='Flag to limit to sites from which the user group is an '
                                                            'admin or users in site that have the admin role')
get_parser.add_argument('by_users', type=inputs.boolean, help='If specified, returns roles by users instead of by user'
                                                              'groups')
get_parser.add_argument('with_usergroups', type=inputs.boolean, help='Used with id_site. Also return user groups that '
                                                                   'don\'t have any access to the site')

post_parser = reqparse.RequestParser()
post_parser.add_argument('site_access', type=str, location='json', help='Site access to create / update', required=True)

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('id', type=int, help='Site Access ID to delete', required=True)


class QuerySiteAccess(Resource):

    def __init__(self, _api, *args, **kwargs):
        Resource.__init__(self, _api, *args, **kwargs)
        self.module = kwargs.get('flaskModule', None)

    @user_multi_auth.login_required
    @api.expect(get_parser)
    @api.doc(description='Get user roles for sites. Only one  parameter required and supported at once.',
             responses={200: 'Success - returns list of users roles in sites',
                        400: 'Required parameter is missing (must have at least one id)',
                        500: 'Error occured when loading sites roles'})
    def get(self):
        parser = get_parser

        current_user = TeraUser.get_user_by_uuid(session['_user_id'])
        user_access = DBManager.userAccess(current_user)
        args = parser.parse_args()

        access = None
        # If we have no arguments, return bad request
        if not any(args.values()):
            return "SiteAccess: missing argument.", 400

        # Query access for user id
        if args['id_user']:
            user_id = args['id_user']

            if user_id in user_access.get_accessible_users_ids():
                access = user_access.query_site_access_for_user(user_id=user_id, admin_only=args['admins'] is not None)

        # Query access for user group
        if args['id_user_group']:
            if args['id_user_group'] in user_access.get_accessible_users_groups_ids():
                from libtera.db.models.TeraUserGroup import TeraUserGroup
                user_group = TeraUserGroup.get_user_group_by_id(args['id_user_group'])
                access = user_group.get_sites_roles()

        # Query access for site id
        if args['id_site']:
            site_id = args['id_site']
            access = user_access.query_access_for_site(site_id=site_id, admin_only=args['admins'] is not None,
                                                       include_empty_groups=args['with_usergroups'])

        if access is not None:
            access_list = []
            if not args['by_users']:
                for site, site_role in access.items():
                    site_access_json = site.to_json()
                    if site_role:
                        site_access_json['site_access_role'] = site_role['site_role']
                        if site_role['inherited']:
                            site_access_json['site_access_inherited'] = True
                    else:
                        site_access_json['site_access_role'] = None
                    access_list.append(site_access_json)
            else:
                # Find users of each user group
                for site, site_role in access.items():
                    for user in user_access.query_users_for_usergroup(site.id_user_group):
                        site_access_json = {'id_user': user.id_user,
                                            'user_name': user.user_user_group_user.get_fullname(),
                                            'site_access_role': site_role['site_role']}
                        access_list.append(site_access_json)
            return access_list

        # No access, but still fine
        return [], 200

    @user_multi_auth.login_required
    @api.expect(post_parser)
    @api.doc(description='Create/update site access for a user group.',
             responses={200: 'Success',
                        403: 'Logged user can\'t modify this site or user access (site admin access required)',
                        400: 'Badly formed JSON or missing fields(id_user or id_site) in the JSON body',
                        500: 'Database error'})
    def post(self):
        # parser = post_parser

        current_user = TeraUser.get_user_by_uuid(session['_user_id'])
        user_access = DBManager.userAccess(current_user)
        # Using request.json instead of parser, since parser messes up the json!
        json_sites = request.json['site_access']

        if not isinstance(json_sites, list):
            json_sites = [json_sites]

        # Validate if we have everything needed
        json_rval = []
        for json_site in json_sites:
            if 'id_user_group' not in json_site:
                return 'Missing id_user_group', 400
            if 'id_site' not in json_site:
                return 'Missing id_site', 400

            # Check if current user can change the access for that site
            if user_access.get_site_role(site_id=json_site['id_site']) != 'admin':
                return 'Forbidden', 403

            # Do the update!
            try:
                access = TeraSiteAccess.update_site_access(json_site['id_user_group'], json_site['id_site'],
                                                           json_site['site_access_role'])
            except exc.SQLAlchemyError:
                import sys
                print(sys.exc_info())
                return '', 500

            # TODO: Publish update to everyone who is subscribed to site access update...
            if access:
                json_rval.append(access.to_json())

        return jsonify(json_rval)

    @user_multi_auth.login_required
    @api.expect(delete_parser)
    @api.doc(description='Delete a specific site access',
             responses={200: 'Success',
                        403: 'Logged user can\'t delete site access(only user who is admin in that site can remove it)',
                        500: 'Database error.'})
    def delete(self):
        parser = delete_parser

        current_user = TeraUser.get_user_by_uuid(session['_user_id'])
        user_access = DBManager.userAccess(current_user)

        args = parser.parse_args()
        id_todel = args['id']

        site_access = TeraSiteAccess.get_site_access_by_id(id_todel)
        if not site_access:
            return 'No site access to delete.', 500

        # Check if current user can delete
        if user_access.get_site_role(site_access.id_site) != 'admin':
            return '', 403

        # If we are here, we are allowed to delete. Do so.
        try:
            TeraSiteAccess.delete(id_todel=id_todel)
        except exc.SQLAlchemyError:
            import sys
            print(sys.exc_info())
            return 'Database error', 500

        return '', 200

