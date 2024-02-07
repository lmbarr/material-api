# Chemical materials API

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development/testing purposes. 

### Prerequisites

What things you need to install the software and how to install them

* [Python 3.9](https://www.python.org/downloads/)
* Pipenv
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
### Testing with Postman -- Import the Postman collection

To import the Postman collection online, follow these steps.

1. Go to Postman and sign in.
2. Select Import file > Upload files.
3. Open the Material API JSON file located in `/test_postman`
4. Select Import.
5. Have fun!