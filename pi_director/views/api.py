from pyramid.response import Response
from pyramid.view import view_config
from cornice import Service
import logging
import sqlalchemy.exc
from datetime import datetime

from pi_director.models.models import (
    DBSession,
    MyModel,
    Screenshot
    )

screenshot = Service(name='pi_screen', path='/api/v1/screen/{uid}', description="Service to handle insertion and deletion of screenshots")

ping = Service(name='pi_ping', path='/api/v1/ping/{uid}', description="Enable tracking of pi last seen")

@ping.get()
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


@screenshot.get()
def view_api_screenshow_show(request):
    uid=request.matchdict['uid']
    shot=DBSession.query(Screenshot).filter(Screenshot.uuid==uid).first()
    response = Response(content_type='image/png')
    response.app_iter=shot.image
    response.content_length = len(shot.image)
    return response

@screenshot.post()
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


