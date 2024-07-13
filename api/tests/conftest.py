# tests/conftest.py
import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models import Base
import configparser
import urllib.parse
from fastapi.testclient import TestClient


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


def load_db_config():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "db_config.ini")
    config.read(config_path)

    env_config = config["database_dev"]
    return env_config
    # db_password = urllib.parse.quote_plus(env_config["api_user_password"])

    # return f"postgresql://{env_config['api_user_username']}:{db_password}@{env_config['host']}:{env_config['port']}/{env_config['dbname']}"


def create_db_url(config, is_admin=False):
    user = config["user"] if is_admin else config["api_user_username"]
    password = urllib.parse.quote_plus(
        config["password"] if is_admin else config["api_user_password"]
    )
    return f"postgresql://{user}:{password}@{config['host']}:{config['port']}/{config['dbname']}"


# config = load_db_config()
# ADMIN_DB_URL = create_db_url(config, is_admin=True)
# TEST_DB_URL = create_db_url(config)

ADMIN_DB_URL = os.getenv("DATABASE_URL")
TEST_DB_URL = os.getenv("DATABASE_URL")

# engine = create_engine(DEV_DB_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    admin_engine = create_engine(ADMIN_DB_URL)
    Base.metadata.create_all(bind=admin_engine)
    admin_engine.dispose()


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(TEST_DB_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        engine.dispose()
        # Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def teardown_test_db():
    yield
    admin_engine = create_engine(ADMIN_DB_URL)
    Base.metadata.drop_all(bind=admin_engine)
    admin_engine.dispose()


@pytest.fixture(scope="function")
def client(db_session):
    from api.main import app, get_db

    # from fastapi.testclient import TestClient

    def override_get_db():
        try:
            # db_session = db_session()
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
