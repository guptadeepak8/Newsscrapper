# This file will contain the code for scraping and summarizing news.
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

def scrape_news(url):
    """
    Scrapes news articles from the given URL.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all the news stories
    articles = soup.find_all('div', class_='eachStory')

    news_items = []
    for article in articles:
        title_element = article.find('h3')
        link_element = article.find('a', {'href': True})

        if title_element and link_element:
            title = title_element.get_text(strip=True)
            link = "https://economictimes.indiatimes.com" + link_element['href']
            news_items.append({'title': title, 'link': link})

    return news_items

def summarize_text(text):
    """
    Summarizes the given text using a pre-trained model.
    """
    summarizer = pipeline('summarization', model='t5-small')
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def get_article_text(url):
    """
    Scrapes the full text of an article from its URL.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('div', class_='artText')
        if article_body:
            return article_body.get_text()
        else:
            return "Could not find article body."
    except Exception as e:
        return f"Error fetching article: {e}"

if __name__ == '__main__':
    # URL of the news website to scrape
    news_url = "https://economictimes.indiatimes.com/markets/stocks/news"

    # Scrape news articles
    news_items = scrape_news(news_url)

    print("--- Top Stock Market News ---")
    # Summarize and display each article
    for item in news_items:
        print(f"**{item['title']}**")
        article_text = get_article_text(item['link'])
        if "Could not find article body." not in article_text and "Error fetching article:" not in article_text:
            summary = summarize_text(article_text)
            print(f"Summary: {summary}")
        else:
            print("Could not summarize article.")
        print("-" * 30)
