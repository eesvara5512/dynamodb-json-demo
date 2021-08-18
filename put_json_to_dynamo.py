import logging
import json

import boto3

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
boto3.set_stream_logger('botocore', level=logging.DEBUG)

TABLE_NAME = 'Products'
client = boto3.client('dynamodb')


def read_json():
    with open('products.json') as json_file:
        data = json.load(json_file)
        for product in data['products']:
            try:  # catch missing key in JSON
                product['priceUsd']['nanos']
            except KeyError:
                product['priceUsd']['nanos'] = 0

            put_products(product)


def put_products(product):
    try:
        client.put_item(
            TableName=TABLE_NAME,
            Item={
                'id': {'S': product['id']},
                'name': {'S': product['name']},
                'description': {'S': product['description']},
                'picture': {'S': product['picture']},
                'price_usd': {
                    'M': {
                        'currency_code': {
                            'S': product['priceUsd']['currencyCode']
                        },
                        'units': {
                            'N': str(product['priceUsd']['units'])
                        },
                        'nanos': {
                            'N': str(product['priceUsd']['nanos'])
                        }
                    }
                },
                'categories': {'SS': product['categories']}
            }
        )
        logger.debug('Event payload: {}'.format(client))
    except Exception as e:
        logger.error(e)


def main():
    read_json()


if __name__ == '__main__':
    main()
