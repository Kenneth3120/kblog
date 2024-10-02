from django.shortcuts import render
from . import models
from .forms import TweetForm
from django.shortcuts import get_object_or_404, redirect
from models import Tweet
# Create your views here.
# Performing crud operations in this file

def index(request):
    return render(request, 'index.html')

# //listing of tweets (Display)

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render (request, 'tweet_list.html', {'tweets':tweets})


# Function to create a new tweet
def tweet_create(request):
    # Checking if method is post
    if request.method == "POST":
        # Then request data from the form that we created in forms.py, also follow the same for files
        form = TweetForm(request.POST, request.FILES)
        # inbuilt method to check if form is valid
        if form.is_valid():
            # Cif valid then save the form.
            tweet = form.save(commit=False)
            # Append the user
            tweet.user = request.user
            # Save the tweet
            tweet.save()
            # redirect the user
            return redirect('tweet_list')   
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})


# //editing the tweet 
def tweet_edit(request, tweet_id):
    # giving edit access to only the user who requested it.
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == "POST":
      form = TweetForm(request.POST, request.FILES, instance=tweet)
      if form.is_valid():
          tweet = form.save(commit=False)
          tweet.user = request.user
          tweet.save()
          return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
        return render(request, 'tweet_form.html', {'form': form})
    
    # deleting the tweet

    def tweet_delete(request, tweet_id):
        tweet = get_object_or_404(Tweet, pk= tweet_id, user = request.user )
        if(request.method == "POST"):
            tweet.delete()
            return redirect('tweet_list')
        return render (request, 'tweet_confirm_delete.html', {'twet': tweet})
        




