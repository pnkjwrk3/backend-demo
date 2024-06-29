import polars as pl
import json
import configparser
from sqlalchemy import create_engine

config = configparser.ConfigParser()
config.read("db_config.ini")

input_json = "playlist.json"

# # load JSON file
# with open("playlist.json") as f:
#     data = json.load(f)


def normalize_json_to_polars(input_json):
    with open(input_json, "r") as f:
        data = json.load(f)

    columns = []

    # loop over all attributes (keys)
    for key, values in data.items():
        # load all values into a list
        column_data = [values[str(i)] for i in range(len(values))]
        # create a polars series and add it to the list
        columns.append(pl.Series(key, column_data))

    df = pl.DataFrame(columns)

    return df


def load_polars_to_sql(df, engine, table_name):

    df.write_database(
        table_name=table_name,
        connection=engine,
        if_table_exists="append",
    )

    return 1


# create a connection to the database
connection_uri = f"postgresql://{config['api_user']['username']}:{config['api_user']['password']}@{config['database']['host']}:{config['database']['port']}/{config['api_user']['dbname']}"
engine = create_engine(connection_uri)

# normalize the JSON data into a polars DataFrame
df = normalize_json_to_polars(input_json)

# load JSON data into SQL database
try:
    load_polars_to_sql(df, engine, "playlist.songs")
    print("Data loaded successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
