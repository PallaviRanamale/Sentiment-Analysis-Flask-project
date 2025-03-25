import re
import time
import tweepy
from textblob import TextBlob
from flask import Flask, request, render_template
from tweepy.errors import TooManyRequests

app = Flask(__name__)

# Provided Twitter API credentials
log = {
    "Keys ": [
        "MyRJXMVqM6E0BmPNXLWR9hHoI",         # consumerKey
        "xGa7nyg1G3mgK17axGBQDWFc5Pws32SuV6tIKeO8N2iqIx64qH",  # consumerSecret
        "AAAAAAAAAAAAAAAAAAAAALSh0AEAAAAAjIsHwGHjVKXn%2BpNjMprvExVVhhg%3DtabLeSRO8Et9pm36U0nl26sVDM80YonCy3MBQpNSnzhRu8ITBW",  # bearer_token
        "1904404434265751552-mMe2uFb6zinIG6ym06OLnBFOkRhhYP",  # accessToken
        "q6g1v3GKhWr8q0IV5q9JUNW7w1jsc1oLtKLmGvPYhwG8Q"        # accessTokenSecret
    ]
}

# Unpack keys from the log dictionary
consumerKey       = log["Keys "][0]
consumerSecret    = log["Keys "][1]
bearer_token      = log["Keys "][2]
accessToken       = log["Keys "][3]
accessTokenSecret = log["Keys "][4]

# Authenticate using OAuthHandler (v1.1) if needed
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
authenticate.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(authenticate, wait_on_rate_limit=True)

# Initialize Tweepy Client for API v2 using the bearer token
client = tweepy.Client(bearer_token=bearer_token)

def clean_tweet(text):
    """
    Remove URLs, mentions, hashtags, and punctuation from tweet text.
    """
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def fetch_tweets_with_retry(user_id, tweet_count, max_attempts=3):
    """
    Fetch tweets with exponential backoff if TooManyRequests error is encountered.
    """
    attempt = 0
    while attempt < max_attempts:
        try:
            tweets_response = client.get_users_tweets(
                id=user_id,
                max_results=min(tweet_count, 100),
                tweet_fields=["lang", "created_at", "text"]
            )
            return tweets_response
        except TooManyRequests:
            wait_time = 60 * (attempt + 1)  # Wait 60, 120, 180 seconds respectively
            print(f"Rate limit reached. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            attempt += 1
    raise TooManyRequests("Rate limit exceeded, maximum retry attempts reached.")

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    results = []
    if request.method == 'POST':
        username = request.form.get('username')
        tweet_count = int(request.form.get('tweet_count', 10))
        try:
            # Get user ID from username using API v2
            user = client.get_user(username=username)
            if not user.data:
                raise ValueError("User not found.")
            user_id = user.data.id

            # Fetch tweets using retry logic
            tweets_response = fetch_tweets_with_retry(user_id, tweet_count)
            if not tweets_response.data:
                raise ValueError("No tweets found for this user.")
            
            # Filter to include only English tweets
            filtered_tweets = [tweet for tweet in tweets_response.data if tweet.lang == "en"]
        except TooManyRequests:
            error = "Rate limit exceeded. Please try again later."
            return render_template("index.html", error=error)
        except Exception as e:
            error = str(e)
            return render_template("index.html", error=error)

        # Process each tweet for sentiment analysis
        for tweet in filtered_tweets:
            original_text = tweet.text
            cleaned_text = clean_tweet(original_text)
            analysis = TextBlob(cleaned_text)
            polarity = analysis.sentiment.polarity
            subjectivity = analysis.sentiment.subjectivity
            sentiment = "Neutral"
            if polarity > 0:
                sentiment = "Positive"
            elif polarity < 0:
                sentiment = "Negative"
            results.append({
                "original_text": original_text,
                "cleaned_text": cleaned_text,
                "sentiment": sentiment,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "created_at": tweet.created_at
            })

        return render_template("results.html", username=username, results=results)
    
    # GET: Render the input form
    return render_template("index.html", error=error)

if __name__ == '__main__':
    app.run(debug=True)
