from pyramid.response import Response
from pyramid.view import view_config
from cornice import Service
import logging
import sqlalchemy.exc
from datetime import datetime

from pi_director.models.models import (
    DBSession,
    MyModel,
    )


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


