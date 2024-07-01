## Json Playlist analysis

#### Backend: FastAPI, SQLAlchemy, Postgres, Pydantic, Pytest

- **Data Processing:**
  - Utilized Polars for JSON to dataframe transformation
  - Initially used DDL commands for database and table creation in Postgres
  - Switched to SQLAlchemy for efficient bulk data insertion

- **Database Interaction:**
  - Employed SQLAlchemy for database querying and result retrieval

- **API Development:**
  - Implemented FastAPI for creating API endpoints
  - Utilized Pydantic for request and response validation

- **Project Structure:**
  - Acknowledged the need for separating database, models, and API code in a production environment

- **Testing:**
  - Implemented Pytest for API endpoint and database query testing
  - Automated DB setup processes using scripts and SQLAlchemy for DEV database configuration

- **Concurrency testing:**
  - Utilized Locust for load testing the API


## Project Setup Instructions

1. **Clone the Repository:**
   ```sh
   git clone <repository_url>
    ```
2. **Create and Activate a Virtual Environment:** 
   ```sh
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install the Required Packages:**
   ```sh
    pip install -r requirements.txt
    ```
4. **Set Up PostgreSQL Databases:**
- Create two PostgreSQL databases, one for development (DEV) and one for production (PROD). 
- The DEV database is for testing, and the PROD database is for the actual API.

5. **Configure the Database:**
- Copy the example configuration file and update the values:
   ```sh
   cp db_config_example.ini db_config.ini
   ```
- Edit `db_config.ini` to include your database credentials, API User credentials and configurations. API User is created using the setup_database.py script.

6. **Create the Database Schema and Tables:**
- For the DEV database:
   ```sh
   python db_admin/setup_database.py dev
   ```
- For the PROD database:
   ```sh
    python db_admin/setup_database.py prod
    ```
7. **Load Data from JSON into the Database:**
- For the DEV database:
   ```sh
   python load_data.py dev
   ```
- For the PROD database:
   ```sh
    python load_data.py prod
    ```
8. **Run the Tests:**
    ```sh
    pytest api/tests
    ```
9. **Run the FastAPI Server:**
    ```sh
    uvicorn api.main:app 
    ```
    Workers can be added using the `--workers` flag. Ideally, gunicorn as a process manager should be used with Uvicorn workers.

    Alternatively, you can use the FastAPI CLI:
    ```sh   
    fastapi run main.py --reload
    ```
10. **Access the API:**
- Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the API.

11. **Load Testing with Locust:**
- Start the Locust server:
    ```sh
    locust -f locustfile.py --host=http://127.0.0.1:8000
    ```
- Open your browser and navigate to `http://127.0.0.1:8089` to access the Locust dashboard.
- Enter the number of users to simulate and the ramp up rate, then click `Start`.
- Monitor the API performance and response times.




Todo:
- [x] Create a database and tables using Polars and Postgres
- [x] Flatten the JSON data and load it into the database as a table
- [x] Create API endpoints using FastAPI
- [x] Setup DEV database using scripts
- [x] Create unit tests using Pytest or any other testing framework
- [x] Take out polars overhead and use SQLAlchemy to load data intodatabase.
- [x] Cleanup the setup_database.py script
- [x] Concurrent testing using Locust
- [ ] Create tests for database connections and permissions.
- [ ] Develop frontend to interact with the API 
- [x] Update pagination to page-per-page in the API

