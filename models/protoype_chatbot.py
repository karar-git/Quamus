"""
stuff to try:
1-generate_text instead of chat
other llms
"""
#from recommendatoin_systems.recom_mod import *
import google.generativeai as genai

genai.configure(api_key="AIzaSyA4MILwVj31XawUJSt3xmdsS2yDRA3wnGY")

# Initialize the chat model
model = genai.GenerativeModel("gemini-2.0-flash")
chat_session = model.start_chat(
    history=[

        {"role": "model", "parts": [{"text":    
    '''
    You are a helpful assistant specialized in analyzing course queries. When a user provides a query describing what kind of course they want, you must extract the following information:

    1. **level**: The proficiency level the user is asking for (e.g., Beginner, Intermediate, Advanced, or mixed), only those levels are available.
    2. **skills**: A list of skills or topics mentioned in the query.
    3. **course_type**: Whether the user is referring to a project-based course or a traditional course, if mentioned. the values could only be "course" or "project"
    4. **Duration**: the duration of the course in hours, inference it to estimated number if enough infos are available. short courses around 2, mid about 15, and long around 30 hourse. return a number not a text
    5. **provider**: the platform that provide the course or project, coursera or edx only

    Your answer should follow exactly this format (no extra text):

    level: <detected level>
    skills: <comma-separated list of skills>
    type : <detected course type, or "N/A" if not specified>
    Duration: <Duration, or "N/A" if no enough information to inference>
    provider: <platform, N/A if not specified>

    For example, if the user query is:
    "I need an advanced Python course focused on deep learning and NLP that includes hands-on projects."

    Your output should be:

    level: Advanced
    skills: Python, Deep Learning, NLP
    type: Project
    Duration: N/A
    provider: N/A
    '''}]}
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

def extract_features(message):
    global chat_session
    response = chat_session.send_message(message)  # Send message using chat
    #if "PROCEED" ==response.text:
    #    results = my_model.predit(someinputs, message)
    #    return chat_session.format_recommendations(results, message)
    return response.text

print(extract_features('what up? i wanna a practical course for linear algebra, from edx and small one, am still new to the field'))
