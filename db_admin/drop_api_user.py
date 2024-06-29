import psycopg2
import configparser


def drop_api_user(schema="public"):
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
    # api_password = config["api_user"]["password"]
    schema = config["api_user"]["schema"]

    try:
        # revoke connect privilege
        cur.execute(
            f"revoke connect on database {config['database']['dbname']} from {api_username}"
        )

        # revoke all privileges on schema
        cur.execute(f"revoke all privileges on schema {schema} from {api_username}")

        # revoke all privileges on all tables in schema
        cur.execute(
            f"revoke all privileges on all tables in schema {schema} from {api_username}"
        )

        # revoke all privileges on all sequences in schema
        cur.execute(
            f"revoke all privileges on all sequences in schema {schema} from {api_username}"
        )

        # revoke all privileges on all functions in schema
        cur.execute(
            f"revoke all privileges on all functions in schema {schema} from {api_username}"
        )

        # revoke default privileges on tables
        cur.execute(
            f"alter default privileges in schema {schema} revoke all privileges on tables from {api_username}"
        )

        # revoke default privileges on sequences
        cur.execute(
            f"alter default privileges in schema {schema} revoke all privileges on sequences from {api_username}"
        )

        # drop user
        cur.execute(f"drop user {api_username}")

        print(f"User {api_username} dropped successfully.")

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    drop_api_user()
