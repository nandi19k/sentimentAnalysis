import streamlit as st
import pandas as pd
import sys
from datetime import datetime
from comments import get_youtube_comments
from translations import _translator
from model import model_inference

# Streamlit UI
st.title('YouTube Video - Sentiment Analysis')

# Input fields
api_key = st.text_input('Enter your YouTube Data API key:')
video_id = st.text_input('Enter the YouTube video ID:')
start_date = st.date_input('Start Date')
end_date = st.date_input('End Date')

if st.button('Get Video Comments'):
    if api_key and video_id and start_date and end_date:
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())
        
        # Get the youtube comments for the given videoID
        comments = get_youtube_comments(video_id, api_key, published_after=start_date, published_before=end_date)
        if comments is None:
            st.warning("No comments for this video. Exiting...")

            # Exit the script
            sys.exit()
            
        df = pd.DataFrame(comments)
        print("Youtube comments succesfully fetched!!")

        #df.to_csv('file.csv')

        # Handle multilingual comments by converting to text
        translated_comments = _translator(df)
        print('translation successfully done')

        # Sentiment Analysis
        df = model_inference(df)

        # Temporal Analysis
        df['date'] = pd.to_datetime(df['date'])
        df['date_'] = df['date'].dt.date  # Extract date from timestamp
        df['month'] = df['date'].dt.month
        sentiment_over_time = df.groupby('date_')['label'].value_counts().unstack().fillna(0)
        sentiment_over_time_month = df.groupby('month')['label'].value_counts().unstack().fillna(0)
        
        st.subheader('Temporal Analysis: Sentiment Trends Over Time')
        st.line_chart(sentiment_over_time)
        st.line_chart(sentiment_over_time_month)
        st.subheader('Results')
        st.write(df)
    else:
        st.warning('Please fill in all the input fields.')
