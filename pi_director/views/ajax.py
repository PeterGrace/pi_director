from pyramid.response import Response
from pyramid.view import view_config
from cornice import Service
import pyramid.httpexceptions as exc
import logging
import sqlalchemy.exc
import pdb
from datetime import datetime

from pi_director.models.models import (
    DBSession,
    RasPi,
    Tags
    )

from pi_director.controllers.controllers import get_pi_info

from pi_director.controllers.user_controls import (
    authorize_user,
    delete_user
    )


editMAC = Service(name='PiUrl', path='/ajax/PiUrl/{uid}',
                  description="Get/Set Pi URL Info")

editCommands = Service(name='EditPiCommands', path='/ajax/SendCommands/{uid}',
                       description='Get/Set sendcommands info')

AuthUser = Service(name='AuthUser', path='/ajax/User/{email}',
                   description="Set User authentication")


@editMAC.get(permission='anon')
def view_json_get_pi(request):
    uid = request.matchdict['uid']
    return get_pi_info(uid)


@editMAC.delete(permission='admin')
def view_json_delete_pi(request):
    uid = request.matchdict['uid']
    DBSession.query(RasPi).filter(RasPi.uuid == uid).delete()


@editMAC.post(permission='admin')
def view_json_set_pi(request):
    # TODO: move into controller(s)
    uid = request.matchdict['uid']
    response = request.json_body

    row = DBSession.query(RasPi).filter(RasPi.uuid == uid).first()
    if row is None:
        row = RasPi()
        row.uuid = uid
    row.url = response['url']
    row.description = response['description']
    row.landscape = response['landscape']
    DBSession.add(row)
    DBSession.flush()
    rowdict = {
        'uuid': row.uuid,
        'url': row.url,
        'description': row.description,
        'landscape': row.landscape
    }
    return rowdict


@editCommands.get(permission='admin')
def view_ajax_get_commands(request):
    pass


@editCommands.post(permission='admin')
def view_ajax_set_commands(request):
    return str(request.json_body)


@AuthUser.post(permission='admin')
def view_ajax_set_user_level(request):
    email = request.matchdict['email']
    authorize_user(email)
    return "{'status':'OK'}"


@AuthUser.delete(permission='admin')
def view_ajax_delete_user(request):
    email = request.matchdict['email']
    delete_user(email)
    return "{'status':'OK'}"
