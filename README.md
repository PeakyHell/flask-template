# flask-template
Flask app template for faster creation of web apps with authentication and database already implemented

# Quick-start Guide

## Without Docker

1. Clone the repository
2. Create a virtual environment using :
```
python3 -m venv .venv
```
3. Activate the virtual environment using :
```
source .venv/bin/activate
```
4. Install modules using :
```
pip install -r requirements.txt
```
5. Setup the SQL tables in models.py
6. Initialize the databse using :
```
flask --app website init-db
```
7. Run the application using :
```
flask --app website run --debug
```

## With Docker

1. Build the Docker image using :
```
docker build -t flask-template .
```
2. Run the container using :
```
docker run -p 5000:5000 flask-template
```

# Blueprint creation

1. Copy the blueprint_template.py file
2. Edit the blueprint name and url prefix
3. Import the blueprint in the \__init__.py file
4. Create a folder for your blueprint html files in the templates folder
5. Create your blueprint views