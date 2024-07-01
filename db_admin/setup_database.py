import os
import sys
import configparser
import argparse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import urllib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.models import Base, Song


# load config
def get_config(env):
    config = configparser.ConfigParser()
    config.read("db_config.ini")
    # print(config)
    return config[env]


# database connection
# connection_uri = f"postgresql://{config['database']['user']}:{config['database']['password']}@{config['database']['host']}:{config['database']['port']}/{config['database']['dbname']}"
# engine = create_engine(connection_uri, pool_size=20, max_overflow=0)


# Ensure the schema exists
def create_schema(engine, schema_name):
    # engine.execute(CreateSchema(schema_name, if_not_exists=True))
    with engine.connect() as connection:
        try:
            connection.execute(CreateSchema(schema_name, if_not_exists=True))
            connection.commit()
            print(f"Schema {schema_name} created successfully")
        except SQLAlchemyError as e:
            print(f"Ane error occurred while creating schema: {e}")


# def create_api_user(engine, config):
#     api_username = config["api_user_username"]
#     api_password = config["api_user_password"]
#     schema = config["api_user_schema"]
#     dbname = config["dbname"]

#     with engine.connect() as connection:
#         try:
#             # create user
#             connection.execute(
#                 text(f"create user {api_username} with password '{api_password}'")
#             )

#             # grant connect privilege
#             connection.execute(
#                 text(f"grant connect on database {dbname} to {api_username}")
#             )

#             # grant schema usage (replace 'public' with your schema name if different)
#             connection.execute(
#                 text(f"grant usage on schema {schema} to {api_username}")
#             )

#             # grant table privileges
#             connection.execute(
#                 text(
#                     f"grant select, insert, update, delete on all tables in schema {schema} to {api_username}"
#                 )
#             )

#             # grant sequence usage
#             connection.execute(
#                 text(
#                     f"grant usage on all sequences in schema {schema} to {api_username}"
#                 )
#             )

#             # set default privileges for future tables and sequences
#             connection.execute(
#                 text(
#                     f"alter default privileges in schema {schema} grant select, insert, update, delete on tables to {api_username}"
#                 )
#             )
#             connection.execute(
#                 text(
#                     f"alter default privileges in schema {schema} grant usage on sequences to {api_username}"
#                 )
#             )

#             connection.commit()

#             print(
#                 f"User {api_username} created successfully with API read and write permissions."
#             )
#         except SQLAlchemyError as e:
#             print(f"An error occurred: {e}")


def setup_database(config):
    db_password = urllib.parse.quote_plus(config["password"])
    engine = create_engine(
        f"postgresql://{config['user']}:{db_password}@{config['host']}:{config['port']}/{config['dbname']}"
    )

    create_schema(engine, config["api_user_schema"])

    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")

    # create_api_user(engine, config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="setup DB for dev/prod")
    parser.add_argument("env", choices=["dev", "prod"], help="dev or prod")

    args = parser.parse_args()
    environment = f"database_{args.env}"

    config = get_config(environment)
    setup_database(config)


# create_schema(engine, "playlist")

# create a session
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
