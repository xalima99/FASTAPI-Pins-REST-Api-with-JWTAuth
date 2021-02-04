"""Helper to scrape title from links"""
import requests

hearders = {'headers':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}

def get_title(url):
    try:
        res = requests.get(url, headers=hearders)
        if res.status_code == 200:
            page = res.text
            title=page[page.find('<title>') + 7 : page.find('</title>')]
            return {
                "title": str(title),
                "status": 200
            }
        else:
            return {
                "title": None,
                "status": 400
            }
    except Exception:
        return None
    
    return None
