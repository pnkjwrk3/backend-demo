from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
import urllib.parse
import configparser
import os, sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# # load config
# config = configparser.ConfigParser()
# config.read("db_config.ini")

# env = os.getenv("APP_ENV", "dev")

# env_config = config[f"database_{env}"]
# db_password = urllib.parse.quote_plus(env_config["api_user_password"])

# engine = create_engine(
#     f"postgresql://{env_config['api_user_username']}:{db_password}@{env_config['host']}:{env_config['port']}/{env_config['dbname']}",
#     pool_size=20,
#     max_overflow=30,
# )

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=30)

# create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @event.listens_for(Base.metadata, "before_create")
# def create_schema(target, connection, **kw):
#     connection.execute(CreateSchema(schema_name, if_not_exists=True))


# # init the database
# from api.models import Base, Song


# def create_tables():
#     Base.metadata.create_all(bind=engine)


# def init_db():
#     create_tables()
