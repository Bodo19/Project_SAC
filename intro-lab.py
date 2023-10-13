import json
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.exceptions import APIException
from recombee_api_client.api_requests import *

client = RecombeeClient(
    'bodoinc-dev',
    'FneAwbFU6KVh5z2osK8Hg6eSXxhxoFWRBvNtGEf9zYsBEA4AbRSTbbjuzJ60gBnT',
    region=Region.EU_WEST
)

desired_properties = {
    'title': 'string',
    'asin': 'string',
    'price': 'double',
    'brand': 'string'
}

existing_properties = set()
try:
    existing_properties = set(client.send(ListItemProperties()).keys())
except Exception as e:
    print(f"An error occurred while listing existing properties: {str(e)}")

for property_name, property_type in desired_properties.items():
    if property_name not in existing_properties:
        try:
            client.send(AddItemProperty(property_name, property_type))
            print(f"Added property: {property_name} ({property_type})")
        except Exception as e:
            print(
                f"An error occurred while adding property: {property_name} ({property_type}): {str(e)}")


def upload_items_to_recombee(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            items_data = json.load(file)
            for item in items_data:
                item_id = str(item['asin'])
                client.send(AddItem(item_id))
                print(f"Uploaded item {item_id} to Recombee")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def upload_items_properties(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            items_data = json.load(file)
            for item in items_data:
                item_id = str(item['asin'])
                properties = {key: value for key,
                              value in item.items() if key in desired_properties}
                client.send(SetItemValues(item_id, properties))
                print(f"Uploaded item {item_id} properties to Recombee")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


json_file = '/mnt/c/Users/crist/Desktop/MOCK_DATA.json'

upload_items_to_recombee(json_file)
upload_items_properties(json_file)
