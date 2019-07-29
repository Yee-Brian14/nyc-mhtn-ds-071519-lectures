import mysql.connector
from mysql.connector import errorcode
import config
from datetime import date, datetime, timedelta
import requests
import time

key = config.apiKey
term = 'bars'
location = 'LA'
url_params = {  'term': term.replace(' ', '+'),
                'location': location.replace(' ', '+'),
                'limit' : 50,
                'offset' : 0
             }
url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'Bearer {}'.format(key)}


def connect_to_AWS():
    cnx = mysql.connector.connect(
        host = config.host,
        user = config.user,
        passwd = config.password
    )
    return cnx

## Close the connection
def close_connections():
    cursor.close()
    conn.close()
    
def create_database(cursor, database_name):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database_name))
    except mysql.connector.Error as err:
        ## Catch the error if an error occurs.
        print("Failed creating database: {}".format(err))
        exit(1)

def create_table(dict_of_tables):
    for table_name in dict_of_tables:
        table_query = dict_of_tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_query)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
            
## Drop all tables to refresh
def drop_everything():
    cursor.execute("""DROP TABLE Reviews;""")
    conn.commit()
    cursor.execute("""DROP TABLE Businesses;""")
    conn.commit()
    
## Function to convert our string to a datetime object
def string_to_time(string):
    return datetime.strptime(string,"%Y-%m-%d %H:%M:%S")

# write a function to parse the API response 
# so that you can easily insert the data in to the DB

## A function that parses the API response
## Uploads businesses into our database
    ## For each business, also get its 3 reviews and upload them
def all_business_results(url_params):
    response = requests.get(url, headers=headers, params=url_params)
    num = response.json()['total']
    print('{} total matches found.'.format(num))
    cur = 0
    results = []
    while cur < num and cur < 1000:
        url_params['offset'] = cur
        results.extend(yelp_call_businesses(url_params))
        add_to_businesses(results[cur:])
        time.sleep(1) #Wait a second
        cur += 50
    return results

# write a function to make a call to the DB 
# updates response with new parameters
def yelp_call_businesses(url_params):
    response = requests.get(url, headers=headers, params=url_params)
    data = response.json()['businesses']
    return data

## Function to upload businesses and reviews to the database
## Takes in a list of dictionaries representing our businesses
def add_to_businesses(list_of_businesses):
    for business in list_of_businesses:
        cursor.execute("""
            INSERT INTO Businesses (businessId, businessName, price, rating)
            VALUES (%s, %s, %s, %s)
        """,(business['id'],business['name'],return_key(business,'price'),business['rating']))
        conn.commit()
        ## Function to get the three reviews for the current business
        get_all_reviews(business['id'])
        

# write a function to parse the API response 
# so that you can easily insert the data in to the DB

## Function to get all three reviews for a given businessId
def get_all_reviews(business_id):
    url_2 = f'https://api.yelp.com/v3/businesses/{business_id}/reviews'
    review_response = requests.get(url_2, headers=headers)
    reviews = review_response.json()['reviews']
    for review in reviews:
        ## Add the reviews to the review table
        add_to_reviews(review,business_id)
        
        
## Function to add the reviews to the table
def add_to_reviews(review,business_id):
    cursor.execute("""
            INSERT into Reviews (reviewId, businessId, rating, text, time_created)
            VALUES (%s, %s, %s, %s, %s)""", 
            (review['id'], business_id, review['rating'], return_key(review,'text'), string_to_time(review['time_created'])))
    conn.commit()

## Check if a key exists in a dictionary.
    ## Returns empty string if the key doesn't exist.
    ## Returns the value of the key if it does exist.
def return_key(dictionary, check_key):
    if check_key in dictionary.keys():
        return dictionary[check_key]
    else:
        return ''