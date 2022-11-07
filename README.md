# Reselling Storage API

A project I built due to having trouble keeping track of 
my own personal storage while I was reselling. From then I have added
Authentication, ratelimiting and deployed upon Docker and AWS.


## How to access documentation

go to the url: `http://<ipaddress>/docs`


## Installation locally

Git Clone this repository

```bash
git clone https://github.com/mbdev0/Reselling-API.git
```

cd into the folder

```bash
cd Reselling-API
```

pip install requirements
```bash
pip install -r requirements.txt
```

cd into app/

```bash
cd app/
```

run server locally
```bash
uvicorn main:app --reload
```

## Installation with Docker

Git Clone this repository

Make sure Docker and Docker-Compose is installed

```bash
git clone https://github.com/mbdev0/Reselling-API.git
```

cd into the folder

```bash
cd Reselling-API
```

run docker-compose 

```bash
docker-compose up -d --build
```
