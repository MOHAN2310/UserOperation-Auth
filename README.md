# UserOperation-Auth
This project is a backend API developed using FastAPI and SQLAlchemy. It provides robust functionality for user authentication and management, including creating, updating, and deleting user accounts. The API also includes a health check endpoint to monitor its status.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Project Setup](#project-setup)
4. [Running the Application](#running-the-application)
5. [Running Tests](#running-tests)

## Getting Started
Follow the instructions below to set up and run your FastAPI project.

### Prerequisites
Ensure you have the following installed:

- Python >= 3.12
- PostgreSQL

### Project Setup
1. Clone the project repository:
    ```bash
    git clone https://github.com/MOHAN2310/UserOperation-Auth.git
    ```
   
2. Navigate to the project directory:
    ```bash
    cd UserOperation-Auth/
    ```

3. Create and activate a virtual environment:
    ```bash
    python3 -m venv env
    env/script/activate
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up environment variables by copying the example configuration:
    ```bash
    cp .env.example .env
    ```


## Running the Application
Start the application:
    ```bash
    python3 main.py
    ```


##  Running Tests
To run the tests for the application, use pytest with coverage. The test cases are located in the test_main.py file.
Run the following command to execute tests:
    ```bash
    pytest --cov=main --cov-report=html
    ```

## Containerization
To run the application using Docker:

Build the Docker image:
    ```bash
    docker build -t useroperation-auth .
    ```

Run the Docker container:
    ```bash
    docker run -d -p 8000:8080 --env-file .env --name useroperation-auth-container useroperation-auth
    ```

Verify the application is running by visiting:
    ```bash
    http://localhost:8080
    ```


