## Json Songs and Playlist analysis

#### Backend: FastAPI, SQLAlchemy, Postgres, Pydantic, Pytest
This is a project that involves the analysis of JSON data containing songs. An API is created to load json files and interact with the data. The API provides endpoints to retrieve songs, rate songs and search for songs. The main aim of this project is to demonstrate the use of FastAPI, SQLAlchemy, Pydantic, and Pytest for bulding scalable backends. 

- **Database:**
  - The project uses Postgres as the database for storing the JSON data.
  - alemic is used for database migrations and schema management.
  - SQLAlchemy is used for database interaction and querying.

- **Data Processing:**
  - The API provides an endpoint to load JSON data into the database.
  - The JSON data is flattened, validated and loaded into a Postgres database using SQLAlchemy.

- **API Development:**
  - Implemented FastAPI for creating API endpoints
  - Utilized Pydantic for request and response validation

- **Project Structure:**
  - The project is structured into modules for easy maintenance and scalability.

- **API Endpoints:**
  - The API provides endpoints to retrieve songs, rate songs, search for songs, and load JSON data into the database.
  - Pagination is implemented to return a fixed number of results per page.

- **Testing:**
  - Implemented Pytest for API endpoint and database query testing
  - Utilized Pytest fixtures for setting up and tearing down test environments
  - Testing is not yet autoamted, and uses the same database as the production database.

- **Concurrency testing:**
  - Utilized Locust for load testing the API


## Project Setup Instructions

1. **Clone the Repository:**
   ```sh
   git clone <repository_url>
    ```

2. **Navigate to the project directory:**
    ```sh
    cd backend-fastapi
    ```
3. Run the following command to start the docker containers:
    ```sh
    docker compose up --build
    ```

4. **Access the API:**
- Open your browser and navigate to `http://0.0.0.0:8000/docs` to access the API.
- The API documentation provides information on the available endpoints and how to interact with them.

4. To stop the docker containers, run the following command:
    ```sh
    docker compose down
    ```


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
- [x] Update pagination to page-per-page in the API

