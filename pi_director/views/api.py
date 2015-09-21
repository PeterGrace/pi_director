from pyramid.response import Response
from pyramid.view import view_config
from cornice import Service
import logging
import sqlalchemy.exc
from datetime import datetime
from io import BytesIO

from pi_director.models.models import (
    DBSession,
    RasPi,
    Screenshot
    )

from pi_director.controllers.user_controls import make_an_admin
from pi_director.controllers.controllers import get_pi_info
from pi_director.controllers.controllers import get_pi_cmd_info


screenshot = Service(name='pi_screen', path='/api/v1/screen/{uid}',
                     description="Service to handle insertion and deletion of screenshots")

ping = Service(name='pi_ping', path='/api/v1/ping/{uid}',
               description="Enable tracking of pi last seen")
ping2 = Service(name='pi_pingv2', path='/api/v2/ping/{uid}/{ip}',
                description="Enable tracking of pi last seen and its ip address")

authme = Service(name='user_create', path='/api/v1/authorize/{email}',
                 description="Create new admin if none exists already")

get_cache = Service(name='get_cache', path='/api/v1/cache/{uid}',
                    description="return data for the requested pi")

reqcommands = Service(name='pi_reqcmds', path='/api/v2/reqcmds/{uid}',
                      description="handle arbitary commands to be run on the pi")


@screenshot.post(permission='anon')
def view_api_screenshot_save(request):
    uid = request.matchdict['uid']
    imgblob = request.POST['screenshot'].file

    '''first, delete previous screenshot'''
    DBSession.query(Screenshot).filter(Screenshot.uuid == uid).delete()

    '''Now, lets make a new screenshot'''
    foo = Screenshot()
    foo.uuid = uid
    foo.image = imgblob.read()
    DBSession.add(foo)
    DBSession.flush()


@screenshot.get(permission='admin')
def view_api_screenshow_show(request):
    uid = request.matchdict['uid']
    shot = DBSession.query(Screenshot).filter(Screenshot.uuid == uid).first()
    if shot:
        with BytesIO() as ss:
            ss.write(shot.image)
            return Response(content_type='image/png', content_length=len(ss.getvalue()), body=ss.getvalue())
    else:
        with BytesIO() as ss:
            emptypng = '89504E470D0A1A0A0000000D49484452000000010000000108000000003A7E9B550000000A4944' \
                       '4154789C63FA0F0001050102CFA02ECD0000000049454E44AE426082'.decode('hex')
            ss.write(emptypng)
            return Response(content_type='image/png', content_length=len(ss.getvalue()), body=ss.getvalue())


@ping.get(permission='anon')
def view_api_ping(request):
    uid = request.matchdict['uid']

    now = datetime.now()

    row = DBSession.query(RasPi).filter(RasPi.uuid == uid).first()
    if row is None:
        row = RasPi()
        row.uuid = uid
        row.url = "http://www.stackexchange.com"
        row.landscape = True
        row.description = ""

    row.lastseen = now
    DBSession.add(row)
    DBSession.flush()


@ping2.get(permission='anon')
def view_api_ping_v2(request):
    uid = request.matchdict['uid']
    ip = request.matchdict['ip']

    now = datetime.now()

    row = DBSession.query(RasPi).filter(RasPi.uuid == uid).first()
    if row is None:
        row = RasPi()
        row.uuid = uid
        row.url = "http://www.stackexchange.com"
        row.landscape = True
        row.description = ""

    row.lastseen = now
    row.ip = ip
    DBSession.add(row)
    DBSession.flush()


@authme.get(permission='anon')
def view_api_create_user(request):
    return make_an_admin(request)


@get_cache.get(permission='anon')
def view_json_get_pi(request):
    uid = request.matchdict['uid']
    return get_pi_info(uid)


@reqcommands.post(permission='admin')
def view_api_reqcommands_results(request):
    pass


@reqcommands.get(permission='anon')
def view_api_reqcommands_get(request):
    cmdinfo = get_pi_cmd_info(request.matchdict['uid'])
    
    return get_pi_cmd_info(uid)
