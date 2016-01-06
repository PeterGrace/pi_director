import pyramid.session
from pyramid.response import Response
from pyramid.view import view_config
import json
import pdb
from sqlalchemy.orm.exc import (
    NoResultFound
)

from pi_director.models.models import DBSession
from pi_director.models.UserModel import UserModel

from pyramid.httpexceptions import HTTPFound, HTTPForbidden

from pyramid.security import remember, forget

@view_config(
  context='velruse.AuthenticationComplete',
  renderer='pi_director:templates/AuthComplete.mak',
)
def login_complete_view(request):
  context = request.context
  result = {
    'provider_type': context.provider_type,
    'provider_name': context.provider_name,
    'profile': context.profile,
    'credentials': context.credentials,
  }
  email = context.profile['verifiedEmail']
  try:
    User = DBSession.query(UserModel).filter(UserModel.email==email).one()
  except NoResultFound, e:
    User = UserModel()
    User.email = email
    User.AccessLevel = 1
    DBSession.add(User)
    DBSession.flush()

  loc = request.route_url('home', _query=(('next', request.path),))

  headers = remember(request, User.email)
  return HTTPFound(location=loc, headers=headers)


@view_config(
  context='velruse.AuthenticationDenied',
  renderer='myapp:templates/LoginFailure.mak'
)
def login_denied_view(request):
  return { 'result': 'denied' }


@view_config(route_name='logout')
def logout_view(request):
  headers = forget(request)
  loc = request.route_url('home', _query=(('next', request.path),))
  return HTTPFound(location=loc,headers=headers)

