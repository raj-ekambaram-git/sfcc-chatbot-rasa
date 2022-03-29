# State of Utah - Chatbot

## Introduction

This repository contains the files for the chatbot - `COURTney` built for State of Utah court's website. The chatbot is developed using `RASA` - a machine learning framework for building chatbots. The bot is developed in order to server the end user's case related details and queries.

---

## Maintaining multiple python versions in the system using `pyenv`

1. Install pyenv (used for maintaining multiple python versions in the system) using the following command:

```
$ brew update
$ brew install pyenv
```

2. Add the following command in your .bash_profile or .zshrc depending on the terminal you use:

```
$ eval "$(pyenv init --path)"
```

The above command sets the path to pyenv when the terminal is loaded.

3. Install new python version using pyenv using the following command:

```
$ pyenv install 3.7.4
```

The above command could fail if `Xcode` is not installed or if one is using BigSur. In that case use the following command:

```
CFLAGS="-I$(brew --prefix openssl)/include -I$(brew --prefix bzip2)/include -I$(brew --prefix readline)/include -I$(xcrun --show-sdk-path)/usr/include" LDFLAGS="-L$(brew --prefix openssl)/lib -L$(brew --prefix readline)/lib -L$(brew --prefix zlib)/lib -L$(brew --prefix bzip2)/lib" pyenv install --patch 3.7.4 < <(curl -sSL https://github.com/python/cpython/commit/8ea6353.patch\?full_index\=1)
```

4. To check the python versions you’ve installed in the system, use the command:

```
$ pyenv versions
```

The output would be:

```
*system
 3.7.4
```

`system` is the base python and `3.7.4` is the additional version installed using `pyenv`. By default `system` is used.

5. In order to change the version being used, use the following command:

```
$ pyenv global 3.7.4
```

---

## Creating virtual environment in python

1. Create a folder named `.virtualenvs` in your root directory
2. Install the python package `virtualenv` using the command:

```
$ pip install virtualenv
```

3. Navigate to the folder `.virtualenvs` and create the virtual environment using the command:

```
$ python -m venv <env_name>
```

4. Activate the environment using the command:

```
$ source <env_name>/bin/activate
```

---

## Installation

To use the chatbot for development, please clone the repo and run:

```
$ pip install -r requirements.txt
```

This will install the bot and all of its requirements.

---

**NOTE:**
This bot should be used with python 3.7.

---

## Generating Swagger client

`swagger-codegen` is used to generate a client to consume REST services. Use the below command to generate a client:

```
$ bash swagger_client_generator.sh
```

If the above command runs successfully, a directory named `client` will be generated in the project root.

---

## Running the Chatbot

Use `rasa train` to train a model. The amount of memory consumed depends upon the training data added to the files.

To run the action server open a new terminal window and run the following command:

```
$ rasa run actions
```

To run the Core/NLU server use the following command:

```
$ rasa run --enable-api --cors "*"
```

In order to include environment variables during server startup, user the following commands to start the server:
Action server:

```
$ python -m server run actions
```

Core/NLU server:

```
$ python -m server run --enable-api --cors "*"
```

---

## Using Docker

Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly.

## One step method:

```
$ cd deployment
$ bash dev_deployment.sh
```

---

## Step by step method:

### To build the images:

For development:

```
$ docker-compose -f docker-compose-local.yml build
```

For production:

```
$ docker-compose build
```

### To spin up containers from the images use:

For development:

```
$ docker-compose -f docker-compose-local.yml up
```

### To push the images to the repository:

Before pushing make sure to login to the account that contains the repository. To login use:

```
$ docker login <account_name>
```

The user will be prompted for the username and password.

For development:

```
$ docker-compose -f docker-compose-local.yml push
```

For production:

```
$ docker-compose push
```

---

### Dev deployment:

Login to the account that contains the repository. To login use:

```
$ docker login <account_name>
```

The user will be prompted for the username and password.

Run the dev deployment script using:

```
$ bash deployment/dev_deployment.sh
```

**NOTE:**
A failed deployment triggered by the script should be redeployed manually by running the commands separately. Using this script to redeploy would push the erroneous image to stable.

---

### Environment variables:

The environment varaibles used by the `core` server are:

1. MONGODB_URL
2. MONGODB_NAME
3. MONGODB_COLLECTION_NAME
4. MONGODB_USERNAME
5. MONGODB_PASSWORD
6. RASA_ACTION_ENDPOINT

The environment varaibles used by the `action` server are:

1. MONGODB_URL
2. MONGODB_NAME
3. MONGODB_COLLECTION_NAME
4. MONGODB_USERNAME
5. MONGODB_PASSWORD
6. MONGODB_ANALYTICS_COLLECTION_NAME
7. MONGODB_FEEDBACK_COLLECTION_NAME
8. MYCASE_BASE_PATH

---

## Pre-commit hooks

The `pre-commit` package has to installed from the `requirements-dev.txt` using the following command:

```
$ pip install -r requirements-dev.txt
```

To add the hooks to the `.git` directory use:

```
$ pre-commit install
```

To update the hooks in the `.pre-commit-config.yaml` file use:

```
$ pre-commit autoupdate
```

To run the hooks on all the files in the repository use:

```
$ pre-commit run --all-files
```

---

## Project overview

- `data/stories` - contains stories

- `data/nlu` - contains NLU training data

- `actions` - contains custom action code

- `domain.yml` - the domain file, including bot response templates

- `config.yml` - training configurations for the NLU pipeline and policy ensemble

---

## Custom socket implementation

The project includes a custom socket implementation that overrides the default implementation provided out-of-the-box by RASA. This is done to accomodate custom authentication between the application and the chatbot. The custom implementation could be found in `custom_socket.py` file. To override the default implementation the reference has been changed from `socketio` to `custom_socket.SocketIOInput` in the `credentials.yml` file.

---

## Authentication

Below is the stepwise representation of the authentication mechanism between the application, chat interface and the chatbot:

1. Botfront makes an authenticate REST call to the MyCase REST server, before sending the first message to RASA.
2. A JWT is returned with an expiry of 30 minutes.
3. Botfront sends this JWT along with the messages to RASA.
4. RASA uses a shared key provided in the `credentials.yml` file to decode the JWT and check its validity. If the JWT is not valid, RASA sends an authentication failure message to Botfront.
5. If the JWT has expired, RASA sends an expiry message along with the current user message to Botfront.
6. Botfront performs Step 1 to get a new JWT and resumes the conversation by resending the current message sent from RASA.

---
