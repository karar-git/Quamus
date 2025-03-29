"""
stuff to try:
1-generate_text instead of chat
other llms
"""
from recommendatoin_systems.recom_mod import *
import google.generativeai as genai

genai.configure(api_key="AIzaSyA4MILwVj31XawUJSt3xmdsS2yDRA3wnGY")

# Initialize the chat model
model = genai.GenerativeModel("gemini-2.0-flash")
chat_session = model.start_chat(
    history=[

        {"role": "model", "parts": [{"text":"""You are a course recommendation assistant. Your task is to check if the user want a recommendations or just asks other questions, if the questions isn't related to the task just tell him am a recommender system only. If all required details are present, respond with: 'PROCEED' only."""}]}
    ]
)


def format_recommendations(results, user_query):
    """
    Uses Gemini to format raw recommendation results into a conversational message.
    
    Args:
        results: The raw output (e.g. a list or dictionary) from your recommendation system.
        user_query: The original user query.
    
    Returns:
        A string with a friendly, conversational message.
    """
    prompt = (
        "You are a helpful assistant that reformats course recommendations in a friendly, personalized way. "
        "The user previously showed interest in courses similar to those below. "
        "Now, the user asked: '{}' \n"
        "Here are the raw recommendations: {} \n"
        "Please generate a conversational response that suggests these courses, mentioning that since the user liked similar topics before, "
        "these courses might be useful."
    ).format(user_query, results)
    
    # Use the Gemini model to generate the formatted response.
    formatted_response = model.generate_content(prompt)
    return formatted_response.text

def chat(message):
    global chat_session
    response = chat_session.send_message(message)  # Send message using chat
    #if "PROCEED" ==response.text:
    #    results = my_model.predit(someinputs, message)
    #    return chat_session.format_recommendations(results, message)
    return response.text


