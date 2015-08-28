"""Pylons bootstrap environment.

Place 'pylons_config_file' into alembic.ini, and the application will
be loaded from there.

"""
from alembic import context
from ConfigParser import ConfigParser
from logging.config import fileConfig
from sqlalchemy.engine.base import Engine
from sqlalchemy import engine_from_config
from pi_director.models.models import Base
from os import path
import pdb


def load_ini(ini_file):
    ini = ConfigParser()
    ini_path = path.join(path.dirname(path.dirname(__file__)), ini_file)
    with open(ini_path,'r') as f:
        ini.readfp(f)
    here = path.abspath(path.join(path.dirname(__file__), '..'))
    return ini



target_metadata = Base.metadata

config = context.config

config_file = config.get_main_option('pyramid_config', '')
ini_file = load_ini(config_file)
sa_url = ini_file.get('app:main', 'sqlalchemy.url')
config.set_main_option('sqlalchemy.url', sa_url)

fileConfig(config_file)


def run_migrations_offline():
    context.configure(
        url=sa_url, target_metadata=target_metadata,
        literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():

    engine = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix='sqlalchemy.',
            )


    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

