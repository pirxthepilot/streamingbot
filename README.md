# streamingbot

Twitch live stream notifier for Slack


## Requirements

* AWS - this tool is designed to run in AWS and makes use of DynamoDB and Lambda
* Python 3.7
* `terraform` for deployment


## Development

It is assumed that all these are running in a a virtualenv.

To set up:

```
pip install -r requirements.txt
python setup.py develop
```

To run the function locally, first set these environment variables:

```
TWITCH_CLIENT_ID
TWITCH_CLIENT_SECRET
SLACK_WEBHOOK_URL
TWITCH_USER
```

then simply:

```
python bot.py
```


## Deployment

This will package the lambda and kick off terraform deployment.

Create a `config.tfvars` file in the `terraform/` directory using [config.tfvars.example](./terraform/config.tfvars.example) as template. Set the values accordingly.

Then run:

```
make package
make deploy
```
