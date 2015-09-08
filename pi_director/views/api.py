from pyramid.response import Response
from pyramid.view import view_config
from cornice import Service
import logging
import sqlalchemy.exc
from datetime import datetime
from io import BytesIO

from pi_director.models.models import (
    DBSession,
    MyModel,
    Screenshot
    )

from pi_director.controllers.user_controls import make_an_admin

screenshot = Service(name='pi_screen', path='/api/v1/screen/{uid}', description="Service to handle insertion and deletion of screenshots")

ping = Service(name='pi_ping', path='/api/v1/ping/{uid}', description="Enable tracking of pi last seen")
ping2 = Service(name='pi_pingv2', path='/api/v2/ping/{uid}/{ip}', description="Enable tracking of pi last seen and its ip address")

authme = Service(name='user_create', path='/api/v1/authorize/{email}', description="Create new admin if none exists already")

@ping2.get(permission='anon')
def view_api_ping_v2(request):
    uid = request.matchdict['uid']
    ip = request.matchdict['ip']

    now=datetime.now()

    row=DBSession.query(MyModel).filter(MyModel.uuid==uid).first()
    if row==None:
        row=MyModel()
        row.uuid=uid
        row.url="http://www.stackexchange.com"
        row.landscape=True
        row.description=""

    row.lastseen=now
    row.ip=ip
    DBSession.add(row)
    DBSession.flush()

@ping.get(permission='anon')
def view_api_ping(request):
    uid = request.matchdict['uid']

    now=datetime.now()

    row=DBSession.query(MyModel).filter(MyModel.uuid==uid).first()
    if row==None:
        row=MyModel()
        row.uuid=uid
        row.url="http://www.stackexchange.com"
        row.landscape=True
        row.description=""

    row.lastseen=now
    DBSession.add(row)
    DBSession.flush()


@screenshot.get(permission='admin')
def view_api_screenshow_show(request):
    uid=request.matchdict['uid']
    shot=DBSession.query(Screenshot).filter(Screenshot.uuid==uid).first()
    with BytesIO() as ss:
        ss.write(shot.image)
        response = Response(content_type='image/png',content_length=len(ss.getvalue()),body=ss.getvalue())
        return response

@screenshot.post(permission='anon')
def view_api_screenshot_save(request):
    uid=request.matchdict['uid']
    imgblob=request.POST['screenshot'].file

    '''first, delete previous screenshot'''
    DBSession.query(Screenshot).filter(Screenshot.uuid==uid).delete()

    '''Now, lets make a new screenshot'''
    foo=Screenshot()
    foo.uuid=uid
    foo.image=imgblob.read()
    DBSession.add(foo)
    DBSession.flush()


@authme.get(permission='anon')
def view_api_create_user(request):

    return make_an_admin(request)
