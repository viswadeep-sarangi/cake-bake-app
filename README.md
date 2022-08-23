# cake-bake-app

### Problem statement
---
Build an app for a small company. The company would like its employees to bake a cake for each other on their birthdays. Write a client and a server app to do so. Server is a REST API server, and client would run various scenarios that the candidate thinks would typically happen.   The server should be python using fastapi, sqlite and sqlalchemy. Client can be in a medium of choice

### How to run
---
- Clone the repository
- This repository assumes the following
    - The computer is running Linux OS
    - Python 3.8 (or higher) is already installed on the computer
- Run the following commands to setup the working environment
```
virtualenv .venv
source .venv/bin/activate
pip install --upgrade pip poetry
poetry install
```
- Ensure that the default environment values set in the `.env` file are appropriate to the usecase
- To create and pre-populate the database, run `pytest` in the terminal
- To run the server
    - Execute the following command in the terminal `poetry run cake-bake-app`, or
    - Run the `__main__.py` file (e.g. `python3 __main__.py`)
- The server should be running now
- The client can be accessed at `localhost:5555` (default) or, at the values set in the `.env` file
