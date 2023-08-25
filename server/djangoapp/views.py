from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, analyze_review_sentiments, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
import requests
from django.http import JsonResponse



# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')



# Create a `login_request` view to handle sign in request
def login_request(request):
     context = {}
    # Handles POST request
     if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect(reverse('admin:index'))
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/login.html', context)
     else:
        return render(request, 'djangoapp/login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect(reverse('djangoapp:index'))



def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password= request.POST['password']

        # Check if user already exists
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except User.DoesNotExist:
            # If not, simply log that this is a new user
            logger.debug("{} is a new user".format(username))

        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)

            # Login the user and redirect to the course list page
            login(request, user)
            return redirect(reverse('admin:index'))
        else:
            return render(request, 'djangoapp/registration.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')



def car_make_list(request):
    car_makes = CarMake.objects.all()
    return render(request, 'djangoapp/car_make_list.html', {'car_makes': car_makes})

def car_model_list(request, car_make_id):
    car_make = CarMake.objects.get(pk=car_make_id)
    car_models = CarModel.objects.filter(car_make=car_make)
    return render(request, 'djangoapp/car_model_list.html', {'car_make': car_make, 'car_models': car_models})



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-gb.functions.cloud.ibm.com/api/v1/namespaces/924940a9-452b-4604-bbe0-d7ba381beb7b/actions/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        dealer = get_dealers_from_cf(dealer_id)
        if dealer:
            reviews = get_dealer_reviews_from_cf(dealer_id)
            for review_obj in reviews:
                review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            dealer.reviews = reviews
            return JsonResponse(dealer)
        else:
            return JsonResponse({"message": "Dealer not found"}, status=404)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)

def add_review(request, dealer_id):
    if request.method == 'POST':
        # Check if user is authenticated

        # Create a review dictionary
        review = {
            "time": datetime.utcnow().isoformat(),
            "dealership": dealer_id,
            "review": request.POST.get("review_text"),  # Get review text from the POST data
            # Add any other attributes you need
        }

        # Create a json_payload dictionary
        json_payload = {
            "review": review,
        }

        # Call post_request method
        response = post_request(url="https://eu-gb.functions.appdomain.cloud/api/v1/web/924940a9-452b-4604-bbe0-d7ba381beb7b/dealership-package/post-review", json_payload=json_payload, dealerId=dealer_id)

        # Print response content (for testing purposes)
        print(response.content)

        # Return the result using HttpResponse
        return HttpResponse(f"Review added successfully: {response.status_code}")

    return render(request, 'add_review.html')  # Render your template








#def get_dealerships(request):
    #context = {}
   # if request.method == "GET":
        #return render(request, 'djangoapp/index.html', context)



# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

