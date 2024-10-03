# Throne and Liberty News and Server Status API

This project implements a RESTful API that scrapes and serves news articles and server status information from the Throne and Liberty game website. It provides endpoints to fetch all news articles, filter articles by category, check server status by region, and monitor the health status of the API and the game website.

## Features

- Fetch all news articles from the Throne and Liberty website
- Filter articles by category
- Paginate through all available news pages
- Check server status for all regions or a specific region
- Health check endpoint
- Full URL links for each article

## Technologies Used

This API is built using the following Python libraries:

- [Robyn](https://github.com/sansyrox/robyn): A fast, asynchronous Python web framework used to create the API endpoints and handle requests.
- [selectolax](https://github.com/rushter/selectolax): A fast HTML parsing library used to extract article and server status information from the webpage.
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

### 2. Get Server Status

- **URL**: `/server-status`
- **Method**: GET
- **Query Parameters**:
  - `region` (optional): Filter server status by region

**Example**:

- Get status for all regions: `GET /server-status`
- Get status for a specific region: `GET /server-status?region=europe`

Available regions:

- western-americas
- eastern-americas
- south-america
- europe
- japan-oceania

### 3. Health Check

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
