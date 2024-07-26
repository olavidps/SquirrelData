
# Squirrel Data

Python ETL Project to test a workflow of uploading and storing squirrels and parks data from CSV files to PostgreSQL
using Python, PySpark

## Prerequisites
- Docker
- Docker compose

## Code structure
```
SquirrelData/
│
├── data/
│   ├── park-data.csv
│   └── squirrel-data.csv
│
├── main.py
├── FileManager.py
├── DatabaseManager.py
├── docker-compose.yaml
├── Dockerfile
├── .env
├── requirements.txt
└── README.md
```

## How to run
```shell
docker-compuse up --build
```

## How it works

Include diagrams

## How to debug
- On PyCharm create a remote python interpreter
- Then Debug the main file as usual

## Troubleshooting

- Docker debug issues

# How to debug
