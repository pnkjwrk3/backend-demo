## Json Playlist analysis

Backend: FastAPI

1. Initially used Polars to transform JSON data into a dataframe and created Database and SQL tables using DDL commands against Postgres.
2. Once the data was loaded into the database, I used SQLAlchemy to query the database and return the results.
3. Used FastAPI to create API endpoints to query the database.
4. While building the API, I used Pydantic to validate the request and response data.
5. As this was a simple model i did not create any folder structure for the project. But in a real world scenario, I would have created a folder structure to separate the database, models, and API code.
6. While setting up the tests, I used Pytest to test the API endpoints and the database queries. However to create a DEV database, I streamlined some of the steps i took earlier to create the database and tables. Database was still manually created, but the roles and tables were setup using scripts and SQLAlchemy.

Steps to run the project:
1. Clone the repository
2. Create a virtual environment and activate it
3. Install the requirements using `pip install -r requirements.txt`
4. Create two Postgres database for the project, one for DEV and one for PROD. The DEV database will be used for testing and the PROD database will be used for the API.
5. Execute `python db_admin/setup_database.py dev` or `python db_admin/setup_database.py prod` to create schema and tables in DEV or PROD database respectively.
6. Load data from JSON into DB using `python load_data.py dev` or `python load_data.py prod`
7. Run the FastAPI server using `uvicorn api.main:app --reload` or `fastapi run main.py --reload`




Todo:
- [x] Create a database and tables using Polars and Postgres
- [x] Flatten the JSON data and load it into the database as a table
- [x] Create API endpoints using FastAPI
- [x] Setup DEV database using scripts
- [ ] Create unit tests using Pytest or any other testing framework
- [x] Take out polars overhead and use SQLAlchemy to load data intodatabase.
- [ ] Cleanup the setup_database.py script

