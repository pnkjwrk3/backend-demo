import json
import configparser
import sys
import argparse
from sqlalchemy import create_engine, text, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
import urllib
from api.models import Base, Song

config = configparser.ConfigParser()
config.read("db_config.ini")

# key_mapping = {"class": "class_field"}


def normalize_json_to_dicts(input_json):
    with open(input_json, "r") as f:
        data = json.load(f)

    n_rows = len(next(iter(data.values())))

    records = []
    for i in range(n_rows):
        record = {}
        for key, values in data.items():
            if key == "class":
                record["class_field"] = values.get(str(i), None)
            else:
                record[key] = values.get(str(i), None)  # handle nulls
            # mapped_key = key_mapping.get(key, key)
            # record[mapped_key] = values.get(str(i), None)
        records.append(record)

    return records


def load_data_to_db(engine, records, chunk_size=10000):
    Session = sessionmaker(bind=engine)
    session = Session()
    # print(records)
    try:
        for i in range(0, len(records), chunk_size):
            chunk = records[i : i + chunk_size]
            session.bulk_insert_mappings(Song, chunk)
            session.commit()
            print(f"Inserted {len(chunk)} records.")
    except exc.SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
        raise
    finally:
        session.close()


def load_main(env, input_json):
    env_config = config[f"database_{env}"]
    db_password = urllib.parse.quote_plus(env_config["api_user_password"])

    engine = create_engine(
        f"postgresql://{env_config['api_user_username']}:{db_password}@{env_config['host']}:{env_config['port']}/{env_config['dbname']}"
    )

    records = normalize_json_to_dicts(input_json)
    print(f"JSON contains {len(records)} records.")

    # Not required in our case, but good to have
    chunk_size = 100000
    load_data_to_db(engine, records, chunk_size)
    print("Data loaded successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load JSON into postgres.")
    parser.add_argument("env", choices=["dev", "prod"], help="dev or prod")
    parser.add_argument("input_json", help="input JSON file")

    args = parser.parse_args()
    load_main(args.env, args.input_json)
