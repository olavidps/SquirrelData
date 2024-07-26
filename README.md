
# Squirrel Data

Python ETL project to demo a workflow of uploading and storing squirrels and parks data from CSV files
in different formats to PostgreSQL using Python, PySpark and Docker

## Features

- Python ETL scripts to process CSV files using Apache Spark through PySpark
- Data is stored in a PostgreSQL Database
- Scripts are allowed to run multiple times without duplication data in the database
- Data from the CSV files has been normalized and stored for these reports:
  - Total of squirrels that are in each Park
  - Total of squirrels that are in each Borough (Area)
  - Total of "Other Animal Sightings" by Park
  - The most common activity for Squirrels
  - Total of all Primary Fur Colors by Park

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


> [!WARNING]  
> Be sure to have a `.env` file before running docker compose. You can rename the `.env.example` file to use it

```shell
docker-compose up --build
```

## Reports
### Prerequisites
- A SQL Client like workbench or IDE extension to connect to the database to execute the reports SQL
- Use the credentials described in the `.env` file

<details>
<summary>Total of squirrels that are in each Park</summary>

```postgresql
SELECT
    park.name AS park_name,
    COUNT(squirrel.id) AS totaltotal_squirrels
FROM parks park
LEFT JOIN squirrels squirrel ON park.id = squirrel.park_id
GROUP BY park.name;
```
</details>

<details>
<summary>Total of squirrels in each Borough (Area)</summary>

```postgresql
SELECT
    area.name AS area_name,
    COUNT(squirrel.id) AS total_squirrels
FROM areas area
JOIN parks park ON area.id = park.area_id
LEFT JOIN squirrels squirrel ON park.id = squirrel.park_id
GROUP BY area.name;
```
</details>

<details>
<summary>Total of "Other Animal Sightings" by Park</summary>

```postgresql
WITH sightings AS (
    SELECT
        park.name AS park_name,
        unnest(string_to_array(park.other_animal_sightings, ',')) AS sighting
    FROM parks park
)
SELECT
    park_name,
    COUNT(*) AS total_sightings
FROM sightings
GROUP BY park_name  LIMIT 100 
```
</details>

<details>
<summary>The most common activity for Squirrels</summary>

```postgresql
SELECT
    activities,
    COUNT(*) AS activity_count
FROM squirrels
GROUP BY activities
ORDER BY activity_count DESC
LIMIT 1;
```
</details>

<details>
<summary>Total of all Primary Fur Colors by Park</summary>

```postgresql
SELECT
    park.name AS park_name,
    color.name AS color_name,
    COUNT(squirrel.id) AS total_squirrels
FROM parks park
JOIN squirrels squirrel ON park.id = squirrel.park_id
JOIN colors color ON squirrel.primary_fur_color_id = color.id
GROUP BY park.name, color.name
ORDER BY park.name, color.name LIMIT 100
```
</details>

## How it works


### General application workflow diagram

![](./img/app_workflow.drawio.svg)

### Entity-relationship diagram

![](./img/entity-relationship.drawio.svg)

### Database Schema diagram

![](./img/database-schema.drawio.svg)

### Class diagram

![](./img/class-diagram.drawio.svg)


## How to debug
- On PyCharm create a remote python interpreter
- Then Debug the main file as usual

## Troubleshooting
- If you have issues debugging with PyCharm check [this thread](https://youtrack.jetbrains.com/issue/PY-58700)
