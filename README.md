# Sentiment Analysis for YouTube Videos

This repository offers a solution to analyze sentiments for a specified YouTube video.

### Approach:
1. **YouTube Comment Scraping:**
   - Utilizes the video's ID to scrape comments from the YouTube platform.
  
2. **Language Standardization:**
   - Converts all extracted comments into a unified language (English) for consistent analysis.

3. **Sentiment Analysis Model:**
   - Employing a pre-trained sentiment analysis model. For simplicity, this example employs the VADER sentiment analysis tool.

4. **Temporal Sentiment Trend Analysis:**
   - Calculates the sentiment trend over a specified time period to reveal fluctuations in sentiment over time.

### How it Works:
1. **Input:** Provide the YouTube video ID.
2. **Process:**
   - Scrapes comments associated with the provided video ID.
   - Standardizes comments to English.
   - Performs sentiment analysis using the chosen model.
   - Computes sentiment trends over the specified time frame.
3. **Output:** Presents sentiment trends graphically, offering insights into sentiment dynamics.

**Live Demo:** https://sentimentt-analysis.streamlit.app/
