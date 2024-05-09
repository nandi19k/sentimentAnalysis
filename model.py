from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Function to perform sentiment analysis
def analyze_sentiment(comment):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(comment)
    
    # Determine sentiment based on compound score
    if sentiment_score['compound'] >= 0.05:
        return 'Positive'
    elif sentiment_score['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'
    

def model_inference(df):
    df['label'] = df['translated_comments'].apply(lambda x:analyze_sentiment(x))
    return df
