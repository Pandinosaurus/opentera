#ifndef WEBAPI_H
#define WEBAPI_H

// TERASERVER URL Definitions
#define WEB_LOGIN_PATH                      "/api/user/login"
#define WEB_LOGOUT_PATH                     "/api/user/logout"
#define WEB_USERINFO_PATH                   "/api/user/users"
#define WEB_SITEINFO_PATH                   "/api/user/sites"
#define WEB_PROJECTINFO_PATH                "/api/user/projects"
#define WEB_SITEACCESS_PATH                 "/api/user/siteaccess"
#define WEB_PROJECTACCESS_PATH              "/api/user/projectaccess"
#define WEB_DEVICEINFO_PATH                 "/api/user/devices"
#define WEB_DEVICESITEINFO_PATH             "/api/user/devicesites"
#define WEB_DEVICEPARTICIPANTINFO_PATH      "/api/user/deviceparticipants"
#define WEB_PARTICIPANTINFO_PATH            "/api/user/participants"
#define WEB_GROUPINFO_PATH                  "/api/user/groups"
#define WEB_SESSIONINFO_PATH                "/api/user/sessions"
#define WEB_SESSIONTYPE_PATH                "/api/user/sessiontypes"

#define WEB_FORMS_PATH                  "/api/user/forms"
#define WEB_FORMS_QUERY_USER_PROFILE    "type=user_profile"
#define WEB_FORMS_QUERY_USER            "type=user"
#define WEB_FORMS_QUERY_SITE            "type=site"
#define WEB_FORMS_QUERY_DEVICE          "type=device"
#define WEB_FORMS_QUERY_PROJECT         "type=project"
#define WEB_FORMS_QUERY_GROUP           "type=group"
#define WEB_FORMS_QUERY_PARTICIPANT     "type=participant"
#define WEB_FORMS_QUERY_SESSION_TYPE    "type=session_type"
#define WEB_FORMS_QUERY_SESSION         "type=session"

#define WEB_QUERY_USERUUID          "user_uuid"
#define WEB_QUERY_ID_USER           "id_user"
#define WEB_QUERY_LIST              "list"
#define WEB_QUERY_ID                "id"
#define WEB_QUERY_ID_SITE           "id_site"
#define WEB_QUERY_ID_PARTICIPANT    "id_participant"
#define WEB_QUERY_ID_PROJECT        "id_project"
#define WEB_QUERY_ID_DEVICE         "id_device"
#define WEB_QUERY_ID_GROUP          "id_group"
#define WEB_QUERY_ID_SESSION        "id_session"

#define WEB_QUERY_AVAILABLE         "available"
#define WEB_QUERY_PARTICIPANTS      "participants"
#define WEB_QUERY_SITES             "sites"

#endif // WEBAPI_H
