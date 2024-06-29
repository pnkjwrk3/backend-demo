import psycopg2
import configparser


def create_api_user(schema="public"):
    config = configparser.ConfigParser()
    config.read("db_config.ini")

    # connect db - admin
    conn = psycopg2.connect(
        host=config["database"]["host"],
        port=config["database"]["port"],
        dbname=config["database"]["dbname"],
        user=config["database"]["user"],
        password=config["database"]["password"],
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Get API user config
    api_username = config["api_user"]["username"]
    api_password = config["api_user"]["password"]
    schema = config["api_user"]["schema"]

    try:
        # create user
        cur.execute(f"create user {api_username} with password '{api_password}'")

        # grant connect privilege
        cur.execute(
            f"grant connect on database {config['database']['dbname']} to {api_username}"
        )

        # grant schema usage (replace 'public' with your schema name if different)
        cur.execute(f"grant usage on schema {schema} to {api_username}")

        # grant table privileges
        cur.execute(
            f"grant select, insert, update, delete on all tables in schema {schema} to {api_username}"
        )

        # grant sequence usage
        cur.execute(
            f"grant usage on all sequences in schema {schema} to {api_username}"
        )

        # set default privileges for future tables and sequences
        cur.execute(
            f"alter default privileges in schema {schema} grant select, insert, update, delete on tables to {api_username}"
        )
        cur.execute(
            f"alter default privileges in schema {schema} grant usage on sequences to {api_username}"
        )

        print(
            f"User {api_username} created successfully with API read and write permissions."
        )

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    create_api_user()
