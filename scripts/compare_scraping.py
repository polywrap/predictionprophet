import streamlit as st
from dotenv import load_dotenv
from prediction_prophet.functions.web_search import web_search
from prediction_prophet.functions.scrape_results import scrape_results, scrape_results_firecrawl

load_dotenv()
st.set_page_config(layout="wide")

query = st.text_input("Enter a query")

if not query:
    st.warning("Please enter a query")
    st.stop()

search = web_search(query)
scrape = scrape_results(search)
fire_scrape = scrape_results_firecrawl(search)

index = int(st.number_input("Index", min_value=0, max_value=len(search) - 1, value=0))

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Tavily's raw content")
    st.write(search[index].url)
    st.write(f"{len((search[index].raw_content or '').split())} words")
    st.markdown("---")
    st.write(search[index].raw_content)

with col2:
    st.markdown("### Scraped content")
    st.write(scrape[index].url)
    st.write(f"{len(scrape[index].content.split())} words")
    st.markdown("---")
    st.write(scrape[index].content)

with col3:
    st.markdown("### FireScraped content")
    st.write(fire_scrape[index].url)
    st.write(f"{len(fire_scrape[index].content.split())} words")
    st.markdown("---")
    st.write(fire_scrape[index].content)
