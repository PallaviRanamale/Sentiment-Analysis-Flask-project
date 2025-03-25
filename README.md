Sentiment Analysis Flask Project

Overview

  This Flask-based web application allows users to input a Twitter username, retrieve their recent tweets in real-time, preprocess the text, and perform sentiment analysis using TextBlob. 
  The application displays the original tweets, the preprocessed versions, and their corresponding sentiment scores.


Features :

  Username Input: Users can enter a Twitter handle to analyze.​
    
   Real-time Tweet Retrieval: Fetches the latest tweets from the specified user.
    
   Text Preprocessing: Cleans and prepares tweet text for analysis.​
    
   Sentiment Analysis: Evaluate the sentiment of each tweet as positive, negative, or neutral using TextBlob.​
    
   Results Display: Shows the original and preprocessed tweets alongside their sentiment scores.


Installation:

  Follow these steps to set up the project on your local machine:

1. Clone the Repository:
   
        git clone https://github.com/PallaviRanamale/Sentiment-analysis-flask-project.git


3. Navigate to the Project Directory:

       cd Sentiment-analysis-flask-project


4. Install Dependencies:

        pip install -r requirements.txt


5. Set Up Twitter API Credentials:

        Create a config.py file in the project directory.



6. Add your Twitter API credentials:

        CONSUMER_KEY = 'your_consumer_key'
        
        CONSUMER_SECRET = 'your_consumer_secret'
        
        ACCESS_TOKEN = 'your_access_token'
        
        ACCESS_TOKEN_SECRET = 'your_access_token_secret'



To run the application:

      python app.py
