from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib.parse
import configparser
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# load config
config = configparser.ConfigParser()
config.read("db_config.ini")

env_config = config[f"database_prod"]  # ideally {os.getenv('ENV', 'dev')}"]
db_password = urllib.parse.quote_plus(env_config["api_user_password"])

engine = create_engine(
    f"postgresql://{env_config['api_user_username']}:{db_password}@{env_config['host']}:{env_config['port']}/{env_config['dbname']}",
    pool_size=20,
    max_overflow=30,
)

# create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
