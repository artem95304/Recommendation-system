# FastAPI Recommender System

This project is an implementation of a recommender system using FastAPI, SQLAlchemy, and a pre-trained machine learning model. It provides recommendations for users based on their historical data.



1. Install the required Python packages:

   ```shell
   pip install -r requirements.txt
   ```

2. Set up your PostgreSQL database and provide the connection details in the `database.py` file.

3. Load your pre-trained machine learning model. Update the path in the `load_models` function in the `main.py` file if necessary.

4. Load your feature data from your database. Update the SQL query and database connection details in the `load_features` function in the `main.py` file.

5. Start the FastAPI server:

   ```shell
   uvicorn app:app --reload
   ```

Now your FastAPI server is up and running.

## API Endpoints

The following API endpoints are available:

- `GET /user/{id}`: Get user details by `id`.
- `GET /post/{id}`: Get post details by `id`.
- `GET /user/{id}/feed`: Get a list of user feed items.
- `GET /post/recommendations/`: Get recommended posts for a user.

## Usage

To use the API, send HTTP requests to the specified endpoints.

### Example Request for Recommended Posts:

```shell
curl -X GET "http://localhost:8000/post/recommendations/?id=203&limit=5"
```

This request fetches the top 5 recommended posts for the user with ID 203.

## Configuration

- Modify the database connection settings in the `database.py` file.
- Update the model path and feature data retrieval in the `main.py` file.

## Contributing

If you want to contribute to this project, please create an issue and discuss it with the maintainers.

