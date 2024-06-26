import os
from prediction_prophet.models.WebScrapeResult import WebScrapeResult
from prediction_prophet.functions.web_search import WebSearchResult
from prediction_prophet.functions.web_scrape import web_scrape
from prediction_prophet.functions.parallelism import par_map
from firecrawl import FirecrawlApp


def scrape_results(results: list[WebSearchResult]) -> list[WebScrapeResult]:
    scraped: list[WebScrapeResult] = par_map(results, lambda result: WebScrapeResult(
        query=result.query,
        url=result.url,
        title=result.title,
        content=web_scrape(result.url),
    ))

    return scraped


def scrape_results_firecrawl(results: list[WebSearchResult]) -> list[WebScrapeResult]:
    app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
    params = {
        "pageOptions": {
            "onlyMainContent": True
        },
    }
    # Can't use par_map here because FirecrawlApp is very rate limited in the free version.
    scraped: list[WebScrapeResult] = [
        WebScrapeResult(
            query=result.query,
            url=result.url,
            title=result.title,
            content=app.scrape_url(result.url, params)["markdown"],
        )
        for result in results
    ]
    return scraped
