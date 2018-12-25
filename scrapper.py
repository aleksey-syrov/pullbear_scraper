from with_csv import csv_writer
from get_json_from_request import fetch_json
import config


'''
    Search Query
'''


def get_count_of_founded_items(query):
    url = f'{config.SEARCH_URL}{query}&{config.BASE_CATALOGUE}&rows={config.ROWS}' \
          f'&lang=en&{config.BASE_STORE}&{config.BASE_WH}'
    data = fetch_json(url)

    return data.get('content').get('numFound')


def search_items_by_query(query, founded_items_count):
    url = f'{config.SEARCH_URL}{query}&{config.BASE_CATALOGUE}&' \
          f'rows={founded_items_count}&lang=en&{config.BASE_STORE}&{config.BASE_WH}'
    data = fetch_json(url)

    return data.get('content').get('docs')


'''
    Item Details
'''


def get_item_data(category, product_id):
    item_base_url = 'https://www.pullandbear.com/itxrest/2/catalog/store/24009400/20109401'
    item_detail_url = f'{item_base_url}/category/{category}/product/{product_id}/detail?languageId=-1&appId=1'

    return fetch_json(item_detail_url)


def img_url_creator(image_url):
    if image_url:
        return f'https://static.pullandbear.net/2/photos{image_url}_1_1_1.jpg'
    return 'No image'


def get_item_details(item_data):
    if item_data:
        item_name = item_data.get('name', 'NoName')
        item_details = item_data.get('detail')
        item_description = item_details.get('longDescription', 'No description')
        image_url = item_details.get('colors')[0].get('image').get('url')

        return {
            'name': item_name,
            'desc': item_description,
            'image': img_url_creator(image_url)
        }
    print('NO DATA')
    return None


def get_items_info(items, founded_items_count):
    total_items_info = []

    print(f'{founded_items_count} was founded...')

    while True:
        slice_count = int(input('How many items you need? '));

        if slice_count <= 0 or slice_count > founded_items_count:
            print(f'Values must be between 1 and {founded_items_count}')
        else:
            break

    for item in items[:int(slice_count)]:
        item_category = item.get('firstRootCategory')
        item_id = item.get('id')

        data = get_item_data(item_category, item_id)
        item_data = get_item_details(data)

        total_items_info.append(item_data)

    return total_items_info


if __name__ == '__main__':
    query = input('Enter query for search: ') or 't-shirt'

    numFound = get_count_of_founded_items(query)

    if numFound:
        items_info = search_items_by_query(query, numFound)
        items = get_items_info(items_info, numFound)

        csv_writer(items, f'{query}.csv')
    else:
        print('No any items')
