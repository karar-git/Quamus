#do not forget to uncomment _generate...
#in the genera, if the skill doesn't exist in the dataset what will happen? if the multilabel assign it to [0,0,0], then it should be good, or depends on how the normalization will behave (will it affect?)
# in the recommend function of the recommender let it update the user personality vector
import google.generativeai as genai
#from various_preprocessing.similarity_preprocessing import user_embedding
import pandas as pd
import re

genai.configure(api_key="AIzaSyA4MILwVj31XawUJSt3xmdsS2yDRA3wnGY")

class CourseRecommenderBot:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.chat = self.model.start_chat()#history=[])
        #self.required_fields = ['skills', 'level']
        self.conversation_history = []
        
        # Initialize with system prompt
        self._append_to_history("system_prompt", '''
        You are a course recommendation expert. Your task is to:
        1. Extract course preferences from user queries
        2. if the user ask about somehting not related to course recommendation tell him am a recommender system only
        3. Maintain natural conversation flow
        4. when wanna recommending responsd with PROCEED
        
        Always respond in EXACTLY ONE of these formats:
        
        [When extracting features]
        description: <the complete query of the user, copy paste his message related to the recommendation, not only the current one, but the old if related to the query of now>
        level: <Beginner|Intermediate|Advanced|mix|N/A>
        skills: <comma-separated list>
        type: <course|project|N/A>
        duration: <number in hours|N/A> if u can inference it, u can like if it is short then around 2 hourse, 15 for mid, 30 for long courses, if u can't inference it just let it be N/A
        provider: <coursera|edx|N/A>
        number_of_recommendation: <maximam is 10, default is 5>
        do not lower the case or capilize it, just as how i wrote it (Beginner not beginner, mix not Mix)

        [When the user asks about something not related to course recommendation]
        NOT RECOMMENDATION: <maintain conversational flow but tell him that this is QUAMUS which is a recommendation system duck >
        ''')
    
    def _append_to_history(self, role, text):
        self.chat.history.append({'role': 'user' if role == 'user' else 'model', 'parts': [{'text': text}]})
        self.conversation_history.append({
            "role": role,
            "content": text,
            "timestamp": len(self.conversation_history)
        })
    
    def _extract_structured_data(self, response):
        pattern = r'(description|level|skills|type|duration|provider|number_of_recommendation):\s*(.*)'
        matches = re.findall(pattern, response)
        return {k: v.strip() for k, v in matches}
    
    #def _needs_clarification(self, data):
    #    missing = [field for field in self.required_fields if not data.get(field) or data[field].lower() == 'n/a']
    #    return missing
    
    def _generate_recommendations(self, criteria, user_input):
        #user_vector = pd.DataFrame(columns = combined_dataset.columns)
        #criteria['skills'] = criteria['skills'].split(',') if criteria['skills'] != "N/A" else ['NaN']
        #for i in criteria.keys[:-1]:
            #if criteria != "N/A"
                #user_vector[i] = criteria[i]
        #user_vector['title'] = ""
        #user_vector = user_embedding(user_vector)
        
        #recommendations = recommender.recommed(user_vector, criteria[-1])
        #formatted_response = self._format_with_llm(recommendations)
        #return formatted_response

        return "help"
    
    def _format_with_llm(self, recommendations):
        # Construct a prompt for the LLM
        prompt = (
            "You are a helpful assistant that formats raw course recommendations into a friendly and "
            "engaging message. The raw recommendations are provided below. Please rephrase them into a beautiful, "
            "conversational response that is easy for the user to understand.\n\n"
            "Raw Recommendations:\n"
            f"{recommendations}\n\n"
            "Formatted Response:"
        )
    
        response = self.model.generate_content(prompt)
        return response.text
    def handle_message(self, user_input):
        # Add user message to history
        self._append_to_history("user", user_input)
        
        # Get AI response
        if user_input == "":
            user_input += " "
        response = self.chat.send_message(user_input).text
        
        # Check response type
        if "NOT RECOMMENDATION:" in response:
            # Clarification needed
            self._append_to_history("assistant", response)
            return response.split("NOT RECOMMENDATION:")[-1].strip()
        
        else:
            # Extract structured data
            data = self._extract_structured_data(response)
            print(data)

            formatted_response= self._generate_recommendations(data, user_input)
            #rec_text = "\n".join(recommendations)
            #formatted_response = f"RECOMMEND: Here are some courses you might like:\n{rec_text}"
            self._append_to_history("assistant", formatted_response)
            return formatted_response

# Usage Example
bot = CourseRecommenderBot()

#I deleted cat flow ,,




#testing comment


