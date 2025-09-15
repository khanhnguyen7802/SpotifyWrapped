# About 

# How to 
- Create an app in [Dashboard](https://developer.spotify.com/dashboard). 
- TODO: create requirements.txt, include: python-dotenv, requests, Flask
- TODO: enter the client id and secret in terminal -> automatically create a .env file in python
- TODO: create schema for each layer 
  - bronze: add the ingested_time column; choose only specific columns 
  - silver: cleaning the data, create dim and fact tables  
    - playlist name can have Unicode escape sequences -> need to decode
    s = "kh\\u00e1nh ng\\u1ee7y\\u00ean"  
    decoded = s.encode("utf-8").decode("unicode_escape")

    - table artist,
  - gold: aggregate value, group by artist top listen, ... 


# Procedure 
1. Databricks for fetching API, while Python + React local app is for front + backend
2. Create resource group (for easy management)
3. Create key vault for storing client_secret 
4. 