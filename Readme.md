<h1 align="center">Cryptocurrency Informer</h1>


### Description  ###

This service fetches cryptocurrency price data from Deribit platform
and provides it via an API. 

### Functions ###

- Fetch price data from deribit platform as per set interval and 
cryptocurrency ticker
- Provide access to cryptocurrency data through API 


### Backend Stack ###

- Python 3.12
- FastAPI(async) 
- PostgreSQL and SQLAlchemy(async)
- Aiohttp
- Gunicorn with Uvicorn workers
- Docker Compose
- Pytest
- Swagger in YAML format, Docstring and Type hint 

### Getting started 

This service is easy to start. Follow  the bellow requirements for Linux (Ubuntu):

#### Clone repository
From the command line: 
```
git clone https://github.com/ssergey-92/cryptocurrency_informer
```

#### Run service:

- From the command line: 
```
cd 'your path to project root directory'
docker compose up --build
```

### Developers ###

Service was develop by Sergey Solop.    
Contact email for suggestions and feedbacks: solop1992@mail.ru  
