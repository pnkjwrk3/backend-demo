## Json Playlist analysis

Backend: FastAPI

1. Initially, I used Polars to transform JSON data into a dataframe and created a database and SQL tables using DDL commands against Postgres. Later I switched to SQLAlchemy to load the data into the database, with bulk insertions.
2. Once the data was loaded into the database, I utilized SQLAlchemy to query the database and retrieve the results.
3. I employed FastAPI to develop API endpoints for querying the database.
4. During the API development, I implemented Pydantic to validate the request and response data.
5. Although this was a simple model, in a real-world scenario, I would have organized the project into a folder structure to separate the database, models, and API code.
6. For testing purposes, I utilized Pytest to test the API endpoints and the database queries. To streamline the process of creating a DEV database, I automated some of the steps by using scripts and SQLAlchemy to set up the roles and tables.

Steps to run the project:
1. Clone the repository
2. Create a virtual environment and activate it
3. Install the requirements using `pip install -r requirements.txt`
4. Create two Postgres database for the project, one for DEV and one for PROD. The DEV database will be used for testing and the PROD database will be used for the API.
5. Execute `python db_admin/setup_database.py dev` or `python db_admin/setup_database.py prod` to create schema and tables in DEV or PROD database respectively.
6. Load data from JSON into DB using `python load_data.py dev` or `python load_data.py prod`
7. Run the tests using `pytest api/tests`
8. Run the FastAPI server using `uvicorn api.main:app --reload` or `fastapi run main.py --reload`




Todo:
- [x] Create a database and tables using Polars and Postgres
- [x] Flatten the JSON data and load it into the database as a table
- [x] Create API endpoints using FastAPI
- [x] Setup DEV database using scripts
- [x] Create unit tests using Pytest or any other testing framework
- [x] Take out polars overhead and use SQLAlchemy to load data intodatabase.
- [x] Cleanup the setup_database.py script
- [ ] Create tests for database connections and permissions.
- [ ] Develop frontend to interact with the API 

