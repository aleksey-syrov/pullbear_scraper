import requests
import json

'''
    Search Query
'''
SEARCH_URL = 'https://api.empathybroker.com/search/v1/query/pullbear/searchv2?q='
ROWS = 0
QUERY = 'boots'
BASE_WH = 'warehouse={}'.format('22109411')
BASE_STORE = 'store={}'.format('24009400')
BASE_CATALOGUE='catalogue={}'.format('20109401')
BASE_URL = f"{SEARCH_URL}{QUERY}&{BASE_CATALOGUE}&rows={ROWS}&lang=en&{BASE_STORE}&{BASE_WH}"


def get_count_of_founded_items(url = BASE_URL):
    data = json.loads(requests.get(url).text)
    return data.get('content').get('numFound')

def search_items_by_query(query = QUERY):
    url = f"{SEARCH_URL}{query}&{BASE_CATALOGUE}&rows={numFound}&lang=en&{BASE_STORE}&{BASE_WH}"
    data = json.loads(requests.get(url).text)
    items_info = data.get('content').get('docs')

    return items_info

'''
    Item Details
'''
ITEM_CATEGORY = '1010141504'
PRODUCT_ID = '501098587'

def get_item_data(category=ITEM_CATEGORY, product_id=PRODUCT_ID):
    ITEM_DETAIL_URL= 'https://www.pullandbear.com/itxrest/2/catalog/store/24009400/20109401'
    item_detail_url = f"{ITEM_DETAIL_URL}/category/{category}/product/{product_id}/detail?languageId=-1&appId=1"

    return json.loads(requests.get(item_detail_url).text)

def get_item_details(item_data):
    item_name = item_data.get('name', 'Unknown')    
    item_details = item_data.get('detail')
    item_description = item_details.get('longDescription')
    default_image_url = item_details.get('colors')[0].get('image').get('url')
    
    return {
        'name': item_name,
        'desc': item_description,
        'image': f"https://static.pullandbear.net/2/photos{default_image_url}_1_1_1.jpg"
    }

numFound = get_count_of_founded_items()

if numFound:
    items_info = search_items_by_query('pants')
else:
    print('No any items')
    items_info = None

for item in items_info[:10]:
    item_category = item.get('firstRootCategory')
    product_id = item.get('id')

    item_data = get_item_data(item_category, product_id)
    print(get_item_details(item_data))