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


editMAC = Service(name='PiUrl', path='/ajax/PiUrl/{uid}', description="Get/Set Pi URL Info")

@editMAC.get()
def view_json_get_pi(request):
    uid=request.matchdict['uid']
    row=DBSession.query(MyModel).filter(MyModel.uuid==uid).first()
    if row==None:
        row=MyModel()
        row.uuid=uid
        row.url="http://www.stackexchange.com"
        row.landscape=True
        row.description=""
        row.lastseen=datetime.now()
        DBSession.add(row)
        DBSession.flush()

    try:
        secs = (datetime.now()-row.lastseen).total_seconds()
    except TypeError:
        secs = -1    
    rowdict={}
    rowdict['uuid']=row.uuid
    rowdict['url']=row.url
    rowdict['lastseen']=secs
    rowdict['description']=row.description
    rowdict['landscape']=row.landscape
    return rowdict

@editMAC.delete()
def view_json_delete_pi(request):
    uid=request.matchdict['uid']
    DBSession.query(MyModel).filter(MyModel.uuid==uid).delete()

@editMAC.post()
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

