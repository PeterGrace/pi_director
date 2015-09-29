from pyramid.response import Response
from pyramid.view import view_config
from cornice import Service
import pyramid.httpexceptions as exc
import logging
import sqlalchemy.exc
import pdb
import operator
import json
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

editCommandResults = Service(name='EditPiCommandResults', path='/ajax/CommandResults/{uid}',
                             description='Get/Set sendcommands info')

AuthUser = Service(name='AuthUser', path='/ajax/User/{email}',
                   description="Set User authentication")

logger = logging.getLogger('ajax')


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
    row.orientation = response['orientation']
    row.browser = response['browser']
    DBSession.add(row)
    DBSession.flush()
    rowdict = {
        'uuid': row.uuid,
        'url': row.url,
        'description': row.description,
        'orientation': row.orientation,
        'browser': row.browser
    }
    return rowdict


@editCommands.post(permission='admin')
def view_ajax_set_commands(request):
    uid = request.matchdict['uid']
    response = request.json_body

    row = DBSession.query(RasPi).filter(RasPi.uuid == uid).first()
    if row is None:
        return '{"status":"error"}'

    # convert response into something with stable sorting
    cmds = []
    tmpcmds = sorted(response.items(), key=operator.itemgetter(0))
    for tmptuple in tmpcmds:
        # extract cmdid/cmd
        cmdid = int(tmptuple[0])
        cmd = tmptuple[1]['cmd']
        del tmptuple[1]['cmd']

        # extract arguments
        tmpargs = sorted(tmptuple[1].items(), key=operator.itemgetter(0))
        args = [item[1] for item in tmpargs]

        # put into our cmd object in the correct order
        cmds.insert(cmdid, {})
        cmds[cmdid]['cmd'] = cmd
        cmds[cmdid]['args'] = args

        # command hasn't been run yet, so this is blank
        cmds[cmdid]['result'] = ''

    row.requested_commands = json.dumps(cmds)
    DBSession.flush()

    return str(cmds)


@editCommandResults.get(permission='admin')
def view_ajax_get_command_results(request):
    uid = request.matchdict['uid']

    row = DBSession.query(RasPi).filter(RasPi.uuid == uid).first()
    if row is None:
        return {'status': 'error'}

    data = json.loads(row.requested_commands)

    return {'status': 'OK', 'data': data}


@editCommandResults.post(permission='admin')
def view_ajax_set_command_results(request):
    uid = request.matchdict['uid']

    row = DBSession.query(RasPi).filter(RasPi.uuid == uid).first()
    if row is None:
        return {'status': 'error'}

    row.requested_commands = ''
    DBSession.flush()

    return {'status': 'OK'}


@AuthUser.post(permission='admin')
def view_ajax_set_user_level(request):
    email = request.matchdict['email']
    authorize_user(email)
    return '{"status":"OK"}'


@AuthUser.delete(permission='admin')
def view_ajax_delete_user(request):
    email = request.matchdict['email']
    delete_user(email)
    return '{"status":"OK"}'

