#pip install --upgrade googletrans==4.0.0-rc1
import requests
import uuid
from googletrans import Translator
import multiprocessing
import pandas as pd
from dotenv import load_dotenv
import os



def _translator(df, target_language = 'en'):

    # Load environment variables from .env file
    load_dotenv()

    # Access environment variables
    key = os.getenv("key")
    endpoint = os.getenv("endpoint")
    location = os.getenv("location")


    # Indicate that we want to translate and the API 
    # version (3.0) and the target language 
    path = '/translate?api-version=3.0'

    # Add the target language parameter 
    target_language_parameter = '&to=' + target_language 

    constructed_url = endpoint + path + target_language_parameter 

    # Set up the header information, which includes our subscription key 
    headers = { 
    'Ocp-Apim-Subscription-Key': key, 
    'Ocp-Apim-Subscription-Region': location, 
    'Content-type': 'application/json', 
    'X-ClientTraceId': str(uuid.uuid4()) 
    }


    try:
        comments = df['text'].values

        translated_comments = [] 
        # Create the body of the request with the text to be translated
        body = [{'text': original_text} for original_text in comments]
        
        print(len(body))
        # Make the call using post 
        translator_request = requests.post(constructed_url, headers=headers, json=body) 

        # Retrieve the JSON response 
        translator_response = translator_request.json()

        #print(translator_response) 
        translated_comments.extend([translator_response[i]['translations'][0]['text'] for i in range(len(body))])
        df['translated_comments'] = translated_comments

    except:
        """
        # Define the number of processes you want to use
        num_processes = multiprocessing.cpu_count()

        # Split the DataFrame into chunks for multiprocessing
        chunk_size = int(len(df)/(num_processes*2))
        chunks = [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]

        # Create a multiprocessing pool
        pool = multiprocessing.Pool(processes=num_processes)

        # Map the translation function to each chunk in parallel
        translated_chunks = pool.map(translate_chunk, chunks)

        # Close the pool to release resources
        pool.close()
        pool.join()

        # Concatenate translated chunks back into one DataFrame
        df = pd.concat(translated_chunks)
        """
        df = translate_chunk(df)

    return df


# Define a function to translate text
def translate_text(text_to_translate):
    # Create a Translator object
    translator = Translator()
    try:
      translated_text = translator.translate(text_to_translate, dest='en')
      return translated_text.text
    except:
      return text_to_translate
    

# Define a function to translate a chunk of data
def translate_chunk(chunk):
    chunk['translated_comments'] = chunk['text'].apply(translate_text)
    return chunk
