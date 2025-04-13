#do not forget to uncomment _generate...
#in the genera, if the skill doesn't exist in the dataset what will happen? if the multilabel assign it to [0,0,0], then it should be good, or depends on how the normalization will behave (will it affect?)
# in the recommend function of the recommender let it update the user personality vector
import google.generativeai as genai
from various_preprocessing.similarity_preprocessing import user_embedding
from recommendatoin_systems.recom_mod import recommend
import pandas as pd
import re

genai.configure(api_key="AIzaSyBAhenlx4qovu_GnrgSswFeapCUbKqLX84")


class CourseRecommenderBot:
    def __init__(self, dataset):
        self.combined_dataset = dataset
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
        Duration: <number in hours|N/A> if u can inference it, u can like if it is short then around 2 hourse, 15 for mid, 30 for long courses, if u can't inference it just let it be N/A
        provider: <coursera|edx|N/A>
        number_of_recommendation: <maximam is 10, default is 5>
        do not lower the case or capilize it, just as how i wrote it (Beginner not beginner, mix not Mix)
        Do Not return emtpy stuff like that {}, and do what i said, restrict ur self to that pattern

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
        pattern = r'(description|level|skills|type|Duration|provider|number_of_recommendation):\s*(.*)'
        matches = re.findall(pattern, response)
        return {k: v.strip() for k, v in matches}
    
    #def _needs_clarification(self, data):
    #    missing = [field for field in self.required_fields if not data.get(field) or data[field].lower() == 'n/a']
    #    return missing
    
    def _generate_recommendations(self, item_embedding, my_vect_model):#criteria, user_input, item_embedding, my_vect_model):#, mlb_skills, normalization_layer, encoder_skills, level_enc, provider_enc, type_enc):
        #@user_vector = pd.DataFrame(columns = self.combined_dataset.columns)
        #@if criteria != {}:
        #@    #criteria['skills'] = criteria['skills'].split(',') if criteria['skills'] != "N/A" else ['NaN']
        #@    #for i in list(criteria.keys())[:-1]:
        #@    #    if criteria[i] != "N/A":
        #@    #       user_vector[i] = criteria[i]
        #@    #user_vector['title'] = ""
        #@    user_vector['description'] = self.holy_message
        #@    user_vector['Duration'] = criteria["Duration"]
        #@else:
        #@    user_vector['description'] = self.holy_message
        #@user_vector = user_embedding(user_vector, my_vect_model, mlb_skills, normalization_layer, encoder_skills, level_enc, provider_enc, type_enc)
        
        recommendations = recommend(self.holy_message, item_embedding, my_vect_model, self.combined_dataset)
        formatted_response = self._format_with_llm(recommendations)#self.combined_dataset[recommendations])
        return formatted_response
    
    def _format_with_llm(self, recommendations):
        # Construct a prompt for the LLM
        prompt = (
            "You are a helpful assistant that formats raw course recommendations into a friendly and "
            "engaging message. The raw recommendations are provided below. Please rephrase them into a beautiful, "
            "conversational response that is easy for the user to understand.\n\n"
            "but becareful, first word should be RECOMMENDED: so i know it is recommendation"
            "Raw Recommendations:\n"
            f"{recommendations}\n\n"
            "Formatted Response:"
        )
    
        response = self.model.generate_content(prompt)
        return response.text
    def handle_message(self, user_input, item_embedding, my_vect_model):#my_vect_model, mlb_skills, normalizatoin_layer, encoder_skills, level_enc, provider_enc, type_enc):
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
            #data = self._extract_structured_data(response)
            #print(data)



            self.holy_message =user_input 
            formatted_response= self._generate_recommendations(item_embedding, my_vect_model ).split("RECOMMENDED: ")[-1].strip()#data, user_input, my_vect_model, mlb_skills, normalizatoin_layer,encoder_skills, level_enc, provider_enc, type_enc)
            #rec_text = "\n".join(recommendations)
            #formatted_response = f"RECOMMEND: Here are some courses you might like:\n{rec_text}"
            self._append_to_history("assistant", formatted_response)
            return formatted_response

# Usage Example
bot = CourseRecommenderBot(pd.read_json('/home/karar/Desktop/recom/data_scraping/preprocessed/combined_dataset.json'))

#I deleted cat flow ,,




#testing comment





