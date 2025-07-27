import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import json

def scrape_news(url):
    """
    Scrapes news articles from the given URL.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
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

def summarize_text(text):
    """
    Summarizes the given text using a pre-trained model.
    """
    summarizer = pipeline('summarization', model='t5-small')
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def calculate_score(title, summary):
    """
    Calculates a score for a news article based on keywords.
    """
    score = 0
    keywords = {
        'high_impact': ['crash', 'surge', 'plunge', 'rally', 'record high', 'record low'],
        'medium_impact': ['earnings', 'profit', 'loss', 'fda', 'approval', 'rate cut'],
        'low_impact': ['analyst', 'opinion', 'expert view']
    }

    text = title.lower() + ' ' + summary.lower()

    for word in keywords['high_impact']:
        if word in text:
            score += 10
    for word in keywords['medium_impact']:
        if word in text:
            score += 5
    for word in keywords['low_impact']:
        if word in text:
            score += 2

    return score

if __name__ == '__main__':
    # URL of the news website to scrape
    news_url = "https://economictimes.indiatimes.com/markets/stocks/news"

    # Scrape news articles
    news_items = scrape_news(news_url)

    articles = []
    # Summarize and display each article
    for item in news_items:
        article_text = get_article_text(item['link'])
        if "Could not find article body." not in article_text and "Error fetching article:" not in article_text:
            summary = summarize_text(article_text)
            score = calculate_score(item['title'], summary)
            articles.append({
                "title": item['title'],
                "summary": summary,
                "score": score
            })

    with open('news.json', 'w') as f:
        json.dump({"articles": articles}, f)
