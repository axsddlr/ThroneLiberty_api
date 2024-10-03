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


if __name__ == "__main__":
    app.start(port=8000)
