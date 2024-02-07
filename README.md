# Chemical materials API

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development/testing purposes. 

### Prerequisites

What things you need to install the software and how to install them

* [Python 3.9](https://www.python.org/downloads/)
* Pipenv
* RabbitMQ
* Docker

### Installing for local development

Clone the project from GitHub

```
git clone https://github.com/lmbarr/material-api
```

Change into the project directory

```
cd material-api
```

Install the project requirements 

```
pipenv install --dev
```

### Running the API with Docker
Clone the repo from github and place a `.env` (request it to me) file in the repository folder.
#### Build and run needed containers

```commandline
docker-compose up -d

```
#### Retrieve an article: hit this endpoint on your prefer browser
```commandline
http://127.0.0.1:5001/article?tracking_number=TN12345679&carrier=UPS
```