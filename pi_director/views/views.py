from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from pyramid.security import authenticated_userid
from pyramid.renderers import render_to_response
from velruse import login_url
from datetime import datetime
import re

import pyramid.httpexceptions as exc
import logging
import sqlalchemy.exc

from pi_director.models.models import (
    DBSession,
    RasPi,
    )

from pi_director.models.UserModel import UserModel

from pi_director.security import (
    groupfinder,
    )

from pi_director.controllers.controllers import (
    get_pis,
    get_logs,
    get_tagged_pis,
    )
from pi_director.controllers.user_controls import get_users


@forbidden_view_config(renderer="pi_director:templates/forbidden.mak")
def forbidden(request):
    logging.info("Going into forbidden")
    m = re.match("^/?(ajax|api).*$", request.path)
    if m is not None:
        '''we're trying to hit an api or ajax query without authentication'''
        logging.warn("Someone tried to hit an ajax/api without authentication.  Route: {route}".format(route=request.path))
        return Response("{'status':'Forbidden'}")

    userid = authenticated_userid(request)
    if userid:
        logging.info("User exists but some other problem occured, FORBIDDEN.")
        group = groupfinder(userid, request)
        logging.info("User {user} access level {access}".format(user=userid, access=group))
        return ("")

    if groupfinder(None, request) is None:
        request.session['goingto'] = request.path
        logging.info("Should be shunting to login page")
        loc = request.route_url('velruse.google-login', _query=(('next', request.path),))
        return exc.HTTPFound(location=loc)


@view_config(route_name='provision', permission='anon')
def view_provision(request):
    response = render_to_response('pi_director:templates/provision.mak', {}, request=request)
    response.content_type = 'text/plain'
    return response


@view_config(route_name='home', renderer="pi_director:templates/home.mak", permission="admin")
def view_home(request):
    logged_in = authenticated_userid(request)
    loginurl = login_url(request, 'google')
    PiList = get_pis()
    return {"loginurl": loginurl, "logged_in": logged_in, "logouturl": request.route_url('logout'), 'pis': PiList}


@view_config(route_name='users', renderer="pi_director:templates/user.mak", permission="admin")
def view_users(request):
    logged_in = authenticated_userid(request)
    loginurl = login_url(request, 'google')
    UserList = get_users()
    return {"loginurl": loginurl, "logged_in": logged_in, "logouturl": request.route_url('logout'), 'users': UserList}


@view_config(route_name='logs', renderer="pi_director:templates/logs.mak", permission='admin')
def view_logs(request):
    uuid = request.matchdict['uuid']
    logs = get_logs(uuid)
    return {"logs": logs, "uuid": uuid}


@view_config(route_name='tagged', renderer="pi_director:templates/home.mak", permission="admin")
def view_tagged(request):
    tags = request.matchdict['tags']
    tagged_pis = get_tagged_pis(tags)

    return {'pis': tagged_pis, 'tags': tags}


@view_config(route_name='wall', renderer="pi_director:templates/wall.mak", permission="user")
def view_wall(request):
    tags = request.matchdict['tags']
    tagged_pis = get_tagged_pis(tags)
    show_list = []
    offline_list = []
    for pi in tagged_pis:
        timediff = datetime.now() - pi.lastseen
        if timediff.total_seconds() <= 300:
            show_list.append(pi)
        else:
            offline_list.append(pi)
    return {'pis': show_list, 'offline': offline_list}


@view_config(route_name='redirectme')
def redirect_me(request):
    uid = request.matchdict['uid']
    url = "http://www.stackexchange.com"
    try:
        row = DBSession.query(RasPi).filter(RasPi.uuid==uid).first()
        if row:
            url = row.url
            logging.info("UID {uid}: {page}".format(uid=row.uuid, page=url))
        else:
            row = RasPi()
            row.uuid = uid
            row.url = "http://www.stackexchange.com"
            row.landscape = True
            row.browser = True
            DBSession.add(row)
            DBSession.flush()
            logging.warn("UID {uid} NOT FOUND. ADDED TO TABLE WITH DEFAULT URL".format(uid=uid))
            url = row.url
    except Exception:
            logging.error("Something went south with DB when searching for {uid}".format(uid=uid))

    raise exc.HTTPFound(url)
