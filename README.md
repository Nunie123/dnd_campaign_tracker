# dnd_campaign_tracker


## Running Locally
1. Go to root directory of repo.
2. `source venv/bin/activate`
3. `flask run --port 5001`

## Database Migrations
1. `flask db init` (only used for initial setup)
2. `flask db migrate`
3. `flask db upgrade`

## Update ECR image from local CLI
1. Authenticate into AWS
2. aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 491085388902.dkr.ecr.us-west-2.amazonaws.com
3. docker build -t cantrip/flask .
4. docker tag cantrip/flask:latest 491085388902.dkr.ecr.us-west-2.amazonaws.com/cantrip/flask:latest
5. docker push 491085388902.dkr.ecr.us-west-2.amazonaws.com/cantrip/flask:latest


## Run Docker Image Locally
1. docker build -t cantrip/flask .
2. docker run -p 5001:5000 cantrip/flask


## Connect to RDS DB loaclly with SQLAlchemy
Execute the following code while in the Python virtual environment:
```python
from sqlalchemy import create_engine
from sqlalchemy import text

sql = text("<add sql script here>")
creds = {
    "username": "<redacted>",
    "password": "<redacted>",
    "host": "<redacted>",
    "port": "3306",
    "database": "prod_cantrip",
}

uri = f"mysql+pymysql://{creds['username']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['database']}"
engine = create_engine(uri)
conn = engine.connect()
result = conn.execute(sql)
```

## Upload new .env config file to S3
1. Authenticate with AWS in command line
2. execute `aws s3 cp .env s3://cantrip-campaigns/flask-app/.env`