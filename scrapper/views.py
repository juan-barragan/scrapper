from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from . import models

# Create your views here.
def scrap(request, max_num_articles):
    themes = ['climate', 'energy', 'ecosystems', 'pollution', 'wildlife', 'policy', 'sci-tech', 'health', 'press-releases', 'agriculture', 'green-building', 'sustainability', 'business']
    urls = [f'https://www.enn.com/{subject}' for subject in themes]
    all_urls_to_scan = list(urls)

    for counter in range(10, max_num_articles, 10):
        for url in urls:
            all_urls_to_scan.append('%s?limit=%d&start=%d' %(url, 10, counter))
    articles = set()
    for url in all_urls_to_scan:
        request = requests.get(url)
        if request.status_code == 200:
            soup = BeautifulSoup(request.text, 'html.parser')
            for anchor in soup.find_all('a'):
                if 'href' in anchor.attrs and 'articles' in anchor.attrs['href']:
                    articles.add(anchor.attrs['href'])
    
    # deal with the articles:
    for article in articles:
        # get the article_id:
        try:
            article_id = int(article.split('/')[2].split('-')[0])
            r = requests.get('https://www.enn.com/' + article )
            soup = BeautifulSoup(r.text, 'html.parser')
            content = soup.select('.article-content')[0].text
            keywords = ','.join([k.text.strip() for k in soup.find('span', itemprop='keywords')])
            # In case article already exist in DB
            try:
                models.Article.objects.create(article_id = article_id, content = content, tags=keywords)
            except:
                pass # TODO: Not satisfying. Certainly article already in database.
        except:
            pass # TODO: not satisfying. Certainly the request went wrong
    
    return HttpResponse('everything is done!')

def get_article(request, article_id):
    article = models.Article.objects.filter(article_id=article_id).first()
    if article:
        return HttpResponse(article.content)
    else:
        return HttpResponse('article %d not found!'%article_id)

def get_article_with_keys(request, keywords):
    individual_keywords = keywords.split(',')
    # retrieve articles containing any keyword
    articles = [models.Article.objects.filter(content__icontains=k) for k in individual_keywords]
    articles_ids = [[a.article_id for a in f] for f in articles]
    articles_result = set(articles_ids[0]).union(*articles_ids)
    articles = [a for f in articles for a in f if a.article_id in articles_result]
    contents = '<br>'.join(['%d<br>%s<br>'%(a.article_id, a.content) for a in articles])
    return HttpResponse(contents)

