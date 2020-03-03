from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
import requests
from time import sleep

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(url):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp
    
    try:
        raw_text = html.select('h1.product_title')[0].get_text().strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None      
    
    try:
        number = html.select('.in-stock')[0].get_text().strip()
        number = number.replace('in stock', '').strip()
        stamp['number'] = number
    except:
        stamp['number'] = None
    
    try:
        price = html.select('.elementor-widget-wrap .woocommerce-Price-amount')[0].get_text().strip()
        price = price.replace('£', '').strip()
        stamp['price'] = price
    except:
        stamp['price'] = None  
    
    try:
        sku = html.select('.sku')[0].get_text().strip()
        stamp['sku'] = sku
    except:
        stamp['sku'] = None  
        
    try:
        category = html.select('.woocommerce-breadcrumb a')[1].get_text().strip()
        stamp['category'] = category
    except:
        stamp['category'] = None  
        
    try:
        subcategory = html.select('.woocommerce-breadcrumb a')[2].get_text().strip()
        stamp['subcategory'] = subcategory
    except:
        stamp['subcategory'] = None         
       
    tags = []   
    try:
        tag_items = html.select('.detail-content a')
        for tag_item in tag_items:
            tag = tag_item.get_text().strip()
            if tag not in tags:
                tags.append(tag)
    except:
        pass    
    
    stamp['tags'] = tags
        
    stamp['currency'] = 'GBP'
    
    # image_urls should be a list
    images = []                    
    try:
        image_items = html.select('.woocommerce-product-gallery__image img')
        for image_item in image_items:
            img = image_item.get('src')
            if img not in images:
                images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
        
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date
    
    stamp['url'] = url
    
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item in html.select('.title a'):
            item_link = item.get('href')
            if item_link not in items:
                items.append(item_link)
    except:
        pass
   
    shuffle(list(set(items)))
    
    return items

def get_categories():
    
    url = 'https://robstineextra.com'
   
    items = []

    try:
        html = get_html(url)
    except:
        return items
    
    try:
        for item in html.select('.mega-menu-link'):
            item_link = item.get('href')
            if (item_link not in items) and ('/product-category/' in item_link): 
                items.append(item_link)
    except: 
        pass
    
    shuffle(list(set(items)))
    
    return items

categories = get_categories()  
for category in categories:
    page_items = get_page_items(category)
    for page_item in page_items:
        stamp = get_details(page_item)  
