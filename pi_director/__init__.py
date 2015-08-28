from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pi_director.models.models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('cornice')
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('redirectme', '/go/{uid}')
    config.add_route('ajax_set_pi','/ajax/set_pi/{uid}/{url}')
    config.add_route('ajax_get_pi','/ajax/get_pi/{uid}')
    config.scan()
    return config.make_wsgi_app()
