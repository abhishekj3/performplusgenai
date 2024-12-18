import streamlit as st
import requests
from openai import AzureOpenAI

# Azure AI configuration
AZURE_API_KEY = "CUCezjchUShB635Ua3YGnJNwScJE3vIGE7yg6qPOZw8JJ0DldvDaJQQJ99ALACYeBjFXJ3w3AAABACOGH3Ff"
AZURE_ENDPOINT = "https://genaisistopenai.openai.azure.com/"

def analyze_text_with_azure(text):
    # Azure Text Analytics endpoint
    url = f"{AZURE_ENDPOINT}/text/analytics/v3.0/sentiment"
    
    # Prepare the request payload
    headers = {"Ocp-Apim-Subscription-Key": AZURE_API_KEY}
    data = {"documents": [{"id": "1", "language": "en", "text": text}]}
    
    # Call Azure AI
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Streamlit app UI
st.title("Productivity Insight")
st.subheader("Analyze text and gain insights with Azure AI")

# Input text from user
user_input = st.text_area("Enter text to analyze:")

if st.button("Analyze"):
    if user_input:
        result = analyze_text_with_azure(user_input)
        
        # Extracting sentiment and confidence scores
        if 'documents' in result and result['documents']:
            sentiment = result['documents'][0]['sentiment']
            confidence_scores = result['documents'][0]['confidenceScores']
            
            # Display results
            st.success("Analysis Result")
            st.text_area(
                label="Sentiment Analysis",
                value=f"Sentiment: {sentiment.capitalize()}\n"
                      f"Confidence Scores:\n"
                      f"  Positive: {confidence_scores['positive']:.2f}\n"
                      f"  Neutral: {confidence_scores['neutral']:.2f}\n"
                      f"  Negative: {confidence_scores['negative']:.2f}",
                height=150
            )
        else:
            st.error("Could not analyze the text. Please try again.")
    else:
        st.warning("Please enter some text!")
