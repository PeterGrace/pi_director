from pyramid.response import Response
from pyramid.view import view_config
import pyramid.httpexceptions as exc
import logging
import sqlalchemy.exc

from pi_director.models.models import (
    DBSession,
    MyModel,
    )

from pi_director.controllers.controllers import (
    get_pis,
    )

@view_config(route_name='home', renderer="pi_director:templates/home.mak")
def view_home(request):
    PiList=get_pis()
    return({'pis':PiList})

@view_config(route_name='redirectme')
def redirect_me(request):
    uid=request.matchdict['uid']
    url="http://www.stackexchange.com"
    try:
        row=DBSession.query(MyModel).filter(MyModel.uuid==uid).first()
        if row:
            url=row.url
            logging.info("UID {uid}: {page}".format(uid=row.uuid,page=url))
        else:
            row=MyModel()
            row.uuid=uid
            row.url="http://www.stackexchange.com"
            row.landscape=True
            DBSession.add(row)
            DBSession.flush()
            logging.warn("UID {uid} NOT FOUND. ADDED TO TABLE WITH DEFAULT URL".format(uid=uid))
            url=row.url
    except Exception:
            logging.error("Something went south with DB when searching for {uid}".format(uid=uid))

    raise exc.HTTPFound(url)
