from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pi_director.models.models import (
    DBSession,
    Base,
    )

from pyramid.security import Allow, Authenticated, Everyone

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.session import SignedCookieSessionFactory

from .security import (groupfinder, LookupUser)

class Root(object):
    __name__ = ''
    __parent__ = None
    __acl__ = [
        (Allow, Everyone, 'anon'),
        (Allow, Authenticated, 'user'),
        (Allow, 'g:admin', 'admin'),
    ]

    def __init__(self, request):
        pass


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    NotSoSecret='CIeUz0RK8fjRq1wJSrID'
    authn_policy = AuthTktAuthenticationPolicy(NotSoSecret,callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    session_factory = SignedCookieSessionFactory(NotSoSecret)



    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings,root_factory=Root)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('velruse.providers.google_oauth2')
    config.set_session_factory(session_factory)
    config.add_google_oauth2_login_from_settings(prefix='velruse.google.')
    config.include('cornice')
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('tagged', '/tagged/{tags}')
    config.add_route('users', '/users')
    config.add_route('logout', '/logout')
    config.add_route('redirectme', '/go/{uid}')
    config.add_route('ajax_set_pi','/ajax/set_pi/{uid}/{url}')
    config.add_route('ajax_get_pi','/ajax/get_pi/{uid}')
    config.add_request_method(LookupUser, 'user', reify=True)
    config.scan()
    return config.make_wsgi_app()
