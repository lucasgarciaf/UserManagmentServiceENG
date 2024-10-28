
# User Manager Service

MVP designed to be both scalable and flexible, catering to our company's continuous growth. As we aim to adopt a microservices architecture, we’re presenting the foundational layer of this venture by developing a User Manager Service.

We’re presenting a RESTful API for managing user data, built with Python, Flask, and .NET 9. This service allows us to create, update, deactivate, and delete users, as well as list all active users.

## Features

- **User Management**: Create, update, deactivate, and delete users.
- **Active and Inactive User Listing**: Retrieve a list of all active or inactive users.
- **Swagger UI**: Interactive API documentation using Swagger (Flasgger).
- **Testing Suite**: Unit tests using pytest.
- **Database**: SQLite database with SQLAlchemy ORM.
- **Platform**: .NET 9, Python & dotnetpython.
- **Version Control**: Git

## Requisites

- **Python**: Version 3.12
- **.NET 9 SDK**

## Installation (using bash)

1. **Clone the Repository**
   ```
   git clone https://github.com/lucasgarciaf/UserManagmentServiceENG
   cd UserManagerServiceENG
   ```

2. **Set Up a Virtual Environment**
   Create and activate a virtual environment to manage dependencies.
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   pip install flask sqlalchemy pytest flasgger
   ```

## Running the Application

1. **Start the Flask Application**
   ```
   python app.py
   ```
   The application will start running at `http://localhost:5000`.

## API Documentation

### Access the Swagger UI
Go to `http://localhost:5000/apidocs/` to access the Swagger UI and see the API endpoints.

## Testing

### Unit Tests
Test using pytest.

- **Run Test File**
  ```
  pytest test_app.py
  ```

## Postman Collection

Check the API endpoints.

1. Open Postman.
2. Click on Import.
3. Select the `UserManagerServiceENG.postman_collection.json` file from the project directory.
4. Click Open.
5. Test the endpoints
