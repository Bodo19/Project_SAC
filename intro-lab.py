import json
import random
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

def send_user_ids(user_ids):
    try:
        for user_id in user_ids:
            client.send(AddUser(user_id))
            print(f"Added user: {user_id}")
    except Exception as e:
        print(f"An error occurred while adding users: {str(e)}")

def submit_user_interactions(user_interactions):
    try:
        for interaction in user_interactions:
            client.send(AddDetailView(interaction['user_id'], interaction['item_id'], timestamp=interaction['timestamp']))
            print(f"Added user interaction: {interaction}")
    except Exception as e:
        print(f"An error occurred while submitting user interactions: {str(e)}")

def request_recommendations(user_id, num_recommendations):
    try:
        response = client.send(RecommendItemsToUser(user_id, num_recommendations))
        recommended_items = response['recomms']
        print(f"Recommended items for user {user_id}: {recommended_items}")
    except Exception as e:
        print(f"An error occurred while requesting recommendations: {str(e)}")

json_file = '/mnt/c/Users/crist/Desktop/Facultate/Master/Anu1_Sem1/SAC/Project_Sac/MOCK_DATA.json'

upload_items_to_recombee(json_file)
upload_items_properties(json_file)

# Function to get a random selection of item IDs from the server
def get_random_items_from_server(count):
    try:
        # Use the ListItems request to get a list of item IDs
        response = client.send(ListItems(count=count))
        return response
    except Exception as e:
        print(f"An error occurred while fetching items from the server: {str(e)}")
        return []


# Define the number of interactions each user will make
interactions_per_user = 3  # Adjust as needed

user_ids = ['user1', 'user2', 'user3']  # Replace with your user IDs
send_user_ids(user_ids)

# Create and submit random interactions for each user
for user_id in user_ids:
    for _ in range(interactions_per_user):
        # Get a random selection of item IDs
        random_item_ids = get_random_items_from_server(interactions_per_user)
        
        # Generate a random timestamp (you can adjust the range as needed)
        random_timestamp = random.randint(0, 999999999)
        
        # Create and submit interactions with the randomly selected items
        user_interactions = [{'user_id': user_id, 'item_id': item_id, 'timestamp': random_timestamp} for item_id in random_item_ids]
        submit_user_interactions(user_interactions)

# Request recommendations for each user
for user_id in user_ids:
    num_recommendations = 5  # Adjust as needed
    request_recommendations(user_id, num_recommendations)
