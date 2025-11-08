# Spotify "Wrapped" me

😞 Sad cuz no one **wrapped** their arms around you? <br>

👉 Don't worry! Spotify got you!

# About

A data pipline that is scheduled to get data from your Spotify, extract the data, load the raw data and perform transformation (ELT).

# Techstack

- Data sources - [Spotify API](https://developer.spotify.com/documentation/web-api)
- Database - Azure Data Lake Storage
- Processor - Azure Databricks
- Orchestration - Azure Data Factory
- Language - Python + PySpark

# Architecture

# Flow

1. A script is triggered every hour to fetch the data via Spotify API using Azure Data Factory.
2. Semi-structured responses are served as raw data, saved as JSON files in `dd:mm:yyyy` format in ADLS Gen2.
3. In Databricks, **external tables** are created to process the data, following the Medallion Architecture.
4. Aggregated data in Gold layer will be fed into PowerBI to build dashboards (_tbd_).
5. If a task is failed during the process, a notification will be sent to Slack channel. Additionally, a summary will be sent weekly to Slack (_tbd_).

# Future plan

- Also integrate the extended streaming history (requested on [Account privacy](https://www.spotify.com/nl-en/account/privacy/)).
- Process automation: enter the client id and secret in terminal -> automatically create a .env file in python

# TODO
- TODO: create requirements.txt, include: python-dotenv, requests, Flask
- TODO: create schema for each layer
  - raw (aka landing): 
  - bronze: add the ingested_time column; choose only specific columns
  - silver: cleaning the data, create dim and fact tables

    - playlist name can have Unicode escape sequences -> need to decode
      s = "kh\\u00e1nh ng\\u1ee7y\\u00ean"  
      decoded = s.encode("utf-8").decode("unicode_escape")

    - table artist,

  - gold: aggregate value, group by artist top listen, ...

# Set up
1. Create an app in [Dashboard](https://developer.spotify.com/dashboard).
2. Create a resource group (for easy management), then create the resources inside this group. 
3. Create key vault for storing client_secret

(tbd)

> For detailed configuration, refer to [configuration.md](./configuration.md).

Things to do right now:
- write a script in Python that fetches Spotify API every hour (PAY ATTENTION TO REFRESH TOKEN)
- later on, we will be using Azure Data Factory to automate that process. 