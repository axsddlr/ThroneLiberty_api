# Throne and Liberty News API

This project implements a RESTful API that scrapes and serves news articles from the Throne and Liberty game website. It provides endpoints to fetch all news articles, filter articles by category, and check the health status of the API and the game website.

## Features

- Fetch all news articles from the Throne and Liberty website
- Filter articles by category
- Paginate through all available news pages
- Health check endpoint
- Full URL links for each article

## Technologies Used

This API is built using the following Python libraries:

- [Robyn](https://github.com/sansyrox/robyn): A fast, asynchronous Python web framework used to create the API endpoints and handle requests.
- [selectolax](https://github.com/rushter/selectolax): A fast HTML parsing library used to extract article information from the webpage.
- [httpx](https://github.com/encode/httpx): A fully featured HTTP client for Python 3, which is used to make requests to the Throne and Liberty website.

## API Endpoints

### 1. Get News Articles

- **URL**: `/news`
- **Method**: GET
- **Query Parameters**:
  - `q` (optional): Filter articles by category

**Example**:

- Get all articles: `GET /news`
- Get articles in the "Update" category: `GET /news?q=Update`
- Get articles in the "General" category: `GET /news?q=General`

### 2. Health Check

- **URL**: `/health`
- **Method**: GET

This endpoint checks the health of the API and its ability to connect to the Throne and Liberty website.

## Installation and Running

1. Clone this repository
2. Install the required packages:

   ```
   pip install robyn selectolax httpx
   ```

3. Run the API:

   ```
   python main.py
   ```

The API will start running on `http://localhost:8000`.

## Note

This API is for educational purposes only. Please be respectful of the Throne and Liberty website's resources and check their terms of service before deploying this in a production environment.
