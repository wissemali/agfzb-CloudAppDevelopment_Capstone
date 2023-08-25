import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth
from .models import DealerReview



def get_request(url, **kwargs):
    api_key = kwargs.get('cg0KXNqw8Z72qK83aBB7AHUNzNfCsoXoEPE1mlWDt8kI')  # Get the API key from kwargs
    params = kwargs.get('params', {})
    
    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_dealers_from_cf(url, api_key=None, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, api_key=api_key)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, dealerId):
    response_data = get_request(url, params={"dealerId": dealerId})
    dealer_reviews = []
    for review_data in response_data:
        review_obj = DealerReview(**review_data)
        sentiment = analyze_review_sentiments(review_obj.review)
        review_obj.sentiment = sentiment
        dealer_reviews.append(review_obj)
    return dealer_reviews 

def analyze_review_sentiments(review):
    api_key = "cg0KXNqw8Z72qK83aBB7AHUNzNfCsoXoEPE1mlWDt8kI"  # Replace with your Watson NLU API key
    if api_key:
        url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/ac29cbf0-9986-4717-9e9f-b83c0e6f1026/v1/analyze"
        params = {
            "text": review,
            "version": "2021-03-25",
            "features": "sentiment",
            "return_analyzed_text": True
        }
        auth = HTTPBasicAuth('apikey', api_key)
        response = get_request(url, params=params, auth=auth)
        sentiment = response.get("sentiment", {}).get("document", {}).get("label")
        return sentiment
    else:
        return None

def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
    return response





# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



