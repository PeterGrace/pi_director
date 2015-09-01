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
    MyModel,
    )
from pi_director.controllers.user_controls import (
    authorize_user,
    delete_user
    )

    


AuthUser = Service(name='AuthUser', path='/ajax/User/{email}', description="Set User authentication")

editMAC = Service(name='PiUrl', path='/ajax/PiUrl/{uid}', description="Get/Set Pi URL Info")

@editMAC.get(permission='anon')
def view_json_get_pi(request):
    uid=request.matchdict['uid']
    row=DBSession.query(MyModel).filter(MyModel.uuid==uid).first()
    if row==None:
        row=MyModel()
        row.uuid=uid
        row.url="http://www.stackexchange.com"
        row.landscape=True
        row.lastseen=datetime.now()
        row.description=""
        DBSession.add(row)
        DBSession.flush()
    rowdict={}
    rowdict['uuid']=row.uuid
    rowdict['url']=row.url
    rowdict['description']=row.description
    rowdict['landscape']=row.landscape
    rowdict['lastseen']=str(row.lastseen)
    return rowdict

@editMAC.delete(permission='admin')
def view_json_delete_pi(request):
    uid=request.matchdict['uid']
    DBSession.query(MyModel).filter(MyModel.uuid==uid).delete()

@editMAC.post(permission='admin')
def view_json_set_pi(request):
    uid=request.matchdict['uid']
    response=request.json_body
    
    row=DBSession.query(MyModel).filter(MyModel.uuid==uid).first()
    if row == None:
        row=MyModel()
        row.uuid=uid
    row.url=response['url']
    row.description=response['description']
    row.landscape=response['landscape']
    DBSession.add(row)
    DBSession.flush()
    rowdict={}
    rowdict['uuid']=row.uuid
    rowdict['url']=row.url
    rowdict['description']=row.description
    rowdict['landscape']=row.landscape
    return rowdict

@AuthUser.post(permission='admin')
def view_ajax_set_user_level(request):
    email=request.matchdict['email']
    authorize_user(email)
    return("{'status':'OK'}")

@AuthUser.delete(permission='admin')
def view_ajax_delete_user(request):
    email=request.matchdict['email']
    delete_user(email)
    return("{'status':'OK'}")
