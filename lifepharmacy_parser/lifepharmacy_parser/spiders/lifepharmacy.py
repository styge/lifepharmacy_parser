import scrapy
from datetime import datetime


class LifepharmacySpider(scrapy.Spider):
    name = "lifepharmacy"
    allowed_domains = ["prodapp.lifepharmacy.com", 'lifepharmacy.com']

    custom_settings = {'DEFAULT_REQUEST_HEADERS': {
        'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'Accept-Language': 'ru-RU',
        'Web-Channel': 'web',
        'Sec-Ch-Ua-Mobile': '?0',
        'Env': 'prod',
        'Longitude': '55.276383',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/127.0.6533.100 Safari/537.36',
        'Uuid': '01J6J4C8S86G412DK87GQVYV3D',
        'Channel': 'web',
        'Latitude': '25.192622'
        }
    }

    categories = ['shampoo', 'whey-protein', 'vitamin-d']
    base_url = ('https://prodapp.lifepharmacy.com/api/web/products?order_by=popularity&type=cols&new_method=true'
                '&lang=ae-en&take=20')

    def start_requests(self):
        for category in self.categories:
            yield scrapy.Request(
                url=f'{self.base_url}&skip=&categories={category}',
                callback=self.parse,
                meta={'category': category, 'start_skip': 0}
            )

    def parse(self, response):
        data = response.json()
        products = data.get('data', {}).get('products', [])
        category = response.meta['category']
        start_skip = response.meta['start_skip']

        if products:
            start_skip += 20
            next_url = f'{self.base_url}&skip={start_skip}&categories={category}'
            yield scrapy.Request(url=next_url, callback=self.parse, meta={'category': category, 'start_skip': start_skip})

        for product in products:
            if 'product_url' not in product:
                continue

            rpc = product['_id']
            product_url = product['product_url']
            full_product_url = f'https://www.lifepharmacy.com/{product_url}'
            title = product['title']

            brand = product['brand']['name'] if product.get('brand') else 'no brand'

            section = []
            for category in product['categories']:
                section.append(category['name'])

            price_data = {}
            for price in product['prices']:
                if price['country_code'] == 'ae':
                    price_data = {'country_code': price['country_code'],
                                  'currency': price['currency'],
                                  'current': price['price']['offer_price'],
                                  'original': price['price']['regular_price']}

                    if price_data['current'] != price_data['original']:
                        current_price = price_data['current']
                        original_price = price_data['original']
                        discount_percentage = round(100 * (1 - current_price / original_price), 2)
                        price_data['sale_tag'] = f"Скидка {discount_percentage}%"
                break

            in_stock_count_product = product['in_stock']
            if in_stock_count_product:
                in_stock = True
                product_count = in_stock_count_product
            else:
                in_stock = False
                product_count = 0

            assets = {}
            assets['main_image'] = product['images']['featured_image']
            assets['set_images'] = []
            if 'gallery_images' in product['images']:
                for image in product['images']['gallery_images']:
                    assets['set_images'].append(image['full'])

            description = product['description']
            description_selector = scrapy.Selector(text=description)
            description = description_selector.xpath('//text()').get().replace('\r\n', '')

            sku = product['sku']
            tax_rate = product['tax_rate']
            need_prescription = product.get('type', '')
            rating = product['rating']
            maximum_salable_qty = product['maximum_salable_qty']



            yield {
                'timestamp': datetime.now(),
                'RPC': rpc,
                'url': full_product_url,
                'title': title,
                'brand': brand,
                'section': section,
                'price_data': price_data,
                'stock': {
                    'in_stock': in_stock,
                    'count': product_count
                },
                'assets': assets,
                'metadata': {
                    '__description': description,
                    'sku': sku,
                    'tax_rate': tax_rate,
                    'need_prescription': need_prescription,
                    'rating': rating,
                    'maximum_salable_qty': maximum_salable_qty
                }
            }
