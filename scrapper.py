import requests
from bs4 import BeautifulSoup

# I have initially tried scrapping from other news sites but some of them didn't allowed scrapping while those
# who allowed, rarely have news mentioning RIL in the past 24 hours. Then i choose 'google news' as it was having
# sufficient news articles of RIL but in it the problem is that since the news is published by various different
# news website there, so i can't target any particular class to access the article text as different
# websites have completely different hierarchy of attributes in their webpages. That's why i am only printing the
# headlines of news articles. I have tried scrapping the article text too(it's code is written in the function
# 'extract_article_content') but its written considering the attribute structure of 'mint' news website so if used
# will publish the content of article also but only for those news that were published from 'mint' on 'goole news'
# mentioning RIL and is not older than 24 hours.

# Function to scrape news articles mentioning RIL from google news
def scrape_news():
    url = "https://news.google.com/search?q=reliance%20industries%20ltd&hl=en-IN&gl=IN&ceid=IN%3Aen"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    res = []
    links = soup.find_all('a', class_='JtKRv')
    dates = soup.find_all('time', class_='hvbAAd')
    valid = []
    for date in dates:
        if date:
            temp = date.get_text(strip=True)
            tmp = temp.split()
            # there are only 3 ways in which dates are given, 1) yesterday, 2) 12 hours/days ago, 3) 12 dec
            # According to given problem statement type 1 is accepted and in type 2 accepted if it is hours(because
            # represented using days only if news is older than 24 hours)and type 3 will not be accepted because
            # only represented if the news is older than yesterday
            if len(tmp) == 1 or (len(tmp) == 3 and (tmp[1] == 'hours' or tmp[1] == 'hour')):
                valid.append(1)
            else:
                valid.append(0)

    i = 0
    for link in links:
        href = link.get('href')
        if href and 'article' in href and valid[i] == 1:
            req_url = href.lstrip('.')
            article_url = 'https://news.google.com'+req_url
            # uncomment this code and the function extract_article_content to publish the article of news published by 'mint'
            # article_content = extract_article_content(article_url)
            article_content = link.get_text()
            res.append({'source': article_url, 'text': article_content})
        i += 1
    return res


# def extract_article_content(article_url):
#     # Fetch the content of the article
#     response = requests.get(article_url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     # Extract article content
#     article_content_holder1 = soup.find_all('div', class_='FirstEle')
#     article_content_holder2 = soup.find_all('div', class_='paywall')
#     article_contents = []
#     for articles in article_content_holder1:
#         article = articles.find('p')
#         if article:
#             article_content = article.get_text(strip=True)
#             article_contents.append(article_content)
#             print(article_content)
#         else:
#             print("No content")
#             break
#     for articles_holder in article_content_holder2:
#         articles = articles_holder.find_all('p', class_=False)
#         for article in articles:
#             if article:
#                 article_content = article.get_text(strip=True)
#                 article_contents.append(article_content)
#             else:
#                 print("No content")
#                 break
#     return article_contents


result = scrape_news()
print(result)

# For scrapping twitter it's asking to create a Developer's account!!
