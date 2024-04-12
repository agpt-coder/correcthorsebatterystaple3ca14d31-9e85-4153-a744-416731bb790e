---
date: 2024-04-12T17:54:52.576348
author: AutoGPT <info@agpt.co>
---

# correcthorsebatterystaple

To create a tool that returns a random xkcd comic each time it is called, the following steps and considerations were gathered based on user requirements and technical research:

1. **Feature Requirements**:
   - The tool should offer additional features beyond simply fetching the comic, such as providing explanations or context for each comic.
   - Users prefer the comic to be random but from a specific range, specifically from the latest 100 comics, to ensure relevance to current events or themes.
   - Implement caching for previously fetched xkcd comics to reduce API calls and load times, enhancing user experience.

2. **Technical Stack**:
   - Programming language: Python, for its ease of handling API requests and data manipulation.
   - API Framework: FastAPI, for creating an asynchronous API that can handle external API requests efficiently.
   - Database: PostgreSQL, for storing information about the cached comics.
   - ORM: Prisma, to interface with the database smoothly and manage data models easily.

3. **Implementation Details**:
   - Utilize the 'random' Python module to select a comic number randomly within the latest 100 comics.
   - Use the public xkcd API to fetch comics based on the generated random number. The API provides necessary details like the comic's title, URL, image link, and alt text without requiring an API key.
   - Integrate the `httpx` library within the FastAPI application to handle asynchronous HTTP requests to the xkcd API.
   - Develop a caching mechanism using PostgreSQL and Prisma to store comic details and serve them on subsequent requests without hitting the xkcd API to reduce load times and API calls.

This project aims to provide users with a seamless experience in discovering xkcd comics, with an emphasis on relevance, speed, and additional contextual insights.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'correcthorsebatterystaple'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
