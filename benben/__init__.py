from benben.models import get_root
from pyramid.config import Configurator
from pyramid.threadlocal import get_current_registry
from sqlalchemy import engine_from_config


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    from benben.models import initialize_sql
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine, drop_all=True)

    config = Configurator(settings=settings, root_factory=get_root)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan()
    return config.make_wsgi_app()


def get_settings():
    return get_current_registry().settings
