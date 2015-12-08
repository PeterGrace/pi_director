from pyramid.response import Response
from pyramid.view import view_config
from cornice import Service
import pdb
import pprint
import json
import logging
import sqlalchemy.exc
from sqlalchemy import and_
from pyramid.httpexceptions import HTTPInternalServerError
from datetime import datetime
from io import BytesIO

from pi_director.models.models import (
    DBSession,
    RasPi,
    Tags,
    Screenshot,
    Logs
    )

from pi_director.controllers.user_controls import make_an_admin
from pi_director.controllers.controllers import get_pi_info
from pi_director.controllers.controllers import get_pi_cmd_info
from pi_director.controllers.controllers import get_log


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

refresh = Service(name='pi_refresh', path='/api/v1/refresh/{uid}',
                  description="send a refresh command request to the pi")

pi_log = Service(name='pi_log', path='/api/v1/pi_log/{uid}',
                 description="Sends Logs from pi to Server")


tags = Service(name='pi_tags', path='/api/v1/tags/{uid}/{tag}')

logger = logging.getLogger('api')


@tags.delete(permission='admin')
def view_api_delete_tag(request):
    uid=request.matchdict['uid']
    tag=request.matchdict['tag']
    DBSession.query(Tags).filter(and_(Tags.uuid == uid,Tags.tag == tag)).delete()


@tags.post(permission='admin')
def view_api_post_new_tag(request):
    uid=request.matchdict['uid']
    tag=request.matchdict['tag']
    newtag = Tags()
    newtag.uuid=uid
    newtag.tag=tag
    DBSession.add(newtag)
    DBSession.flush()


@refresh.get(permission='admin')
def view_api_refresh_get(request):
    uid = request.matchdict['uid']

    refresh_cmd={}
    refresh_cmd['cmd']='su'
    refresh_cmd['args']=['-c','/home/pi/refresh.sh','pi']
    refresh_cmd['result']=''


    row = DBSession.query(RasPi).filter(RasPi.uuid == uid).first()
    if row is None:
        return {'status': 'error'}

    try:
        # If there are already records to be run,
        # we'll start with them in the array already
        cmd_data = json.loads(row.requested_commands)
    except (ValueError, TypeError):
        cmd_data=[]
        pass

    cmd_data.append(refresh_cmd)

    row.requested_commands = json.dumps(cmd_data)
    DBSession.flush()

    return {'status': 'OK'}


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


@screenshot.get(permission='anon')
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


@pi_log.post(permission='anon')
def view_api_log_save(request):
    uid = request.matchdict['uid']
    pi_log = request.POST['pi_log']
    filename = request.POST['filename']
    DBSession.query(Logs).filter(
        Logs.uuid == uid).filter(
        Logs.filename == filename).delete()

    new_log = Logs()
    new_log.filename = filename
    new_log.uuid = uid
    new_log.log = pi_log
    DBSession.add(new_log)
    DBSession.flush()


@pi_log.get(permission='anon')
def view_api_log_show(request):
    uid = request.matchdict['uid']
    filename = request.GET['filename']
    log = get_log(uuid=uid, filename=filename)
    return Response(content_type='text/plain', body=log.log)


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
        row.orientation = 0
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
        row.orientation = 0
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
    piinfo = get_pi_info(uid)


    try:
        cmd_data = json.loads(piinfo['requested_commands'])
        for i, cmdinfo in enumerate(cmd_data):
            try:
                if cmdinfo['result']:
                    piinfo['requested_commands'] = ''
                    break
            except KeyError:
                #There was no result field in the cmd_info structure, lets add it and act like it was always there
                cmdinfo['result']=''        
                piinfo['requested_commands'] = ''
    except (ValueError, TypeError):
        pass            
        

    return piinfo


@reqcommands.post(permission='anon')
def view_api_reqcommands_post(request):
    uid = request.matchdict['uid']
    results = request.json_body
    results['data'] = json.loads(results['data'])

    row = DBSession.query(RasPi).filter(RasPi.uuid == uid).first()
    if row is None:
        return {'status': 'error'}

    cmd_data = json.loads(row.requested_commands)
    new_data = []

    for i, cmdinfo in enumerate(cmd_data):
        if results['status'] == 'OK':
            cmdinfo['result'] = results['data'][i]
        else:
            cmdinfo['result'] = results['msg']

        new_data.append(cmdinfo)

    row.requested_commands = json.dumps(new_data)
    DBSession.flush()

    return {'status': 'OK'}


@reqcommands.get(permission='anon')
def view_api_reqcommands_get(request):
    uid = request.matchdict['uid']

    row = DBSession.query(RasPi).filter(RasPi.uuid == uid).first()
    if row is None:
        return {'status': 'error'}

    cmd_data = json.loads(row.requested_commands)

    return {'status': 'OK', 'data': data}
