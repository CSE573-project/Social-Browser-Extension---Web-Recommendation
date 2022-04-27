from mining import extract_text
from web_recommendation import recommend_web_articles
from user_recommendation import recommend_users

def get_recommendations(links):
    texts = extract_text(links)
    print(texts)
    recommended_links = recommend_web_articles(texts)
    return recommended_links

def get_user_recommendations(links, i):
    texts = []
    for group in links:
        texts.append(extract_text(group))
    print(texts)
    recommended_links = recommend_users(texts, i)
    return recommended_links
