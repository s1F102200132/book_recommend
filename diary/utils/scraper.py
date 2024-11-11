import requests

def get_asin_from_amazon(url):
    """
    Amazonの商品URLからASINを取得する関数。
    
    Parameters:
    url (str): Amazonの商品ページのURL
    
    Returns:
    str: 商品のASIN
    """
    from urllib.parse import urlparse, parse_qs

    parsed_url = urlparse(url)
    if 'amazon.co.jp' in parsed_url.netloc:
        asin = parse_qs(parsed_url.query).get('asin')
        return asin[0] if asin else None
    return None

def get_page_from_amazon(url):
    """
    Amazonの商品ページのコンテンツを取得する関数。
    
    Parameters:
    url (str): Amazonの商品ページのURL
    
    Returns:
    str: 商品ページのHTMLコンテンツ
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text  # HTMLコンテンツを返す
    else:
        return None  # エラー時にはNoneを返す

