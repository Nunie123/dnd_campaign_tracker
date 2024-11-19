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