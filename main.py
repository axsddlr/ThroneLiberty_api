import logging

import httpx
from robyn import Request, Robyn, jsonify
from selectolax.parser import HTMLParser

app = Robyn(__file__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def clean_json(data):
    for item in data:
        for key in item:
            if isinstance(item[key], str):
                item[key] = item[key].strip()
    return data


def fetch_page(url):
    with httpx.Client(follow_redirects=True) as client:
        response = client.get(url)

    if response.status_code != 200:
        logger.error(f"Failed to fetch data from {url}")
        return None

    return response.text


def parse_articles(html_content):
    parser = HTMLParser(html_content)
    articles = parser.css("div.ags-SlotModule")

    articles_data = []

    for article in articles:
        href = article.css_first("a.ags-SlotModule-slotLink").attributes.get("href")
        title = article.css_first(".ags-SlotModule-slotLink-info-heading--blog")
        category = article.css_first(
            ".ags-SlotModule-slotLink-info-subheading--featured"
        )
        description = article.css_first(".ags-SlotModule-slotLink-info-text--blog")

        if all([href, title, category, description]):
            article_dict = {
                "link": f"https://www.playthroneandliberty.com{href}",
                "title": title.text(),
                "category": category.text(),
                "description": description.text(),
            }
            articles_data.append(article_dict)

    return articles_data


@app.get("/news")
async def get_news(request: Request):
    base_url = "https://playthroneandliberty.com/en-us/news-load-more?page="
    page = 1
    all_articles = []

    while True:
        url = f"{base_url}{page}"
        logger.debug(f"Fetching page {page}")

        html_content = fetch_page(url)
        if not html_content:
            break

        articles_data = parse_articles(html_content)
        if not articles_data:
            logger.debug(f"No articles found on page {page}. Stopping.")
            break

        all_articles.extend(articles_data)
        page += 1

    # Clean the JSON data
    all_articles = clean_json(all_articles)

    # Get the 'q' query parameter
    category_filter = request.query_params.get("q")

    if category_filter:
        # Filter articles based on the category
        filtered_articles = [
            article
            for article in all_articles
            if article["category"].lower() == category_filter.lower()
        ]
        logger.debug(
            f"Filtered articles for category '{category_filter}': {len(filtered_articles)}"
        )
    else:
        filtered_articles = all_articles

    logger.debug(
        f"Total articles: {len(all_articles)}, Filtered articles: {len(filtered_articles)}"
    )

    return jsonify(filtered_articles)


@app.get("/server-status")
async def get_server_status(request: Request):
    region = request.query_params.get("region")

    url = "https://www.playthroneandliberty.com/en-us/support/server-status"

    html_content = fetch_page(url)
    if not html_content:
        return jsonify({"error": "Failed to fetch server status data"}), 500

    parser = HTMLParser(html_content)

    all_regions = [
        "western-americas",
        "eastern-americas",
        "south-america",
        "europe",
        "japan-oceania",
    ]

    if region and region not in all_regions:
        return jsonify({"error": "Invalid region"}), 400

    result = {}

    for current_region in all_regions:
        if region and current_region != region:
            continue

        region_div = parser.css_first(f'div[data-regionid="{current_region}"]')
        if not region_div:
            continue

        servers = []
        for server_item in region_div.css(
            "div.ags-ServerStatus-content-serverStatuses-server-item"
        ):
            name = server_item.css_first(
                "span.ags-ServerStatus-content-serverStatuses-server-item-label"
            ).text()
            status_svg = server_item.css_first("svg")

            if "24FF00" in status_svg.html:  # Green color
                status = "Good"
            elif "FFF500" in status_svg.html:  # Yellow color
                status = "Busy"
            elif "FF0000" in status_svg.html:  # Red color
                status = "Full"
            elif "00F0FF" in status_svg.html:  # Blue color
                status = "In-Maintenance"
            else:
                status = "Unknown"

            servers.append({"name": name, "status": status})

        result[current_region] = servers

    return jsonify(result)


@app.get("/health")
async def health_check(request: Request):
    api_status = "healthy"
    api_message = "The API is up and running"

    # Check Throne and Liberty website
    tl_status = "unhealthy"
    tl_message = "Unable to connect to Throne and Liberty website"
    try:
        with httpx.Client(follow_redirects=True) as client:
            response = client.get("https://playthroneandliberty.com")
        if response.status_code == 200:
            tl_status = "healthy"
            tl_message = "Successfully connected to Throne and Liberty website"
    except Exception as e:
        logger.error(f"Error connecting to Throne and Liberty website: {str(e)}")

    # Overall health is healthy only if both API and TL website are healthy
    overall_status = (
        "healthy" if api_status == "healthy" and tl_status == "healthy" else "unhealthy"
    )

    return jsonify(
        {
            "status": overall_status,
            "api": {"status": api_status, "message": api_message},
            "throne_and_liberty": {"status": tl_status, "message": tl_message},
        }
    )


if __name__ == "__main__":
    app.start(port=8000)
