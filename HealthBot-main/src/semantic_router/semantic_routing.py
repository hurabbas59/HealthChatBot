
from src.model.models import call_llm
from src.semantic_router.prompts import (user_intent_identifiction_template, 
                                         conversational_chat_template,
                                         medical_assistance_tempalte,
                                         other_medical_scenerio_template,
                                         book_appointment_template
                                        
                                         )
from langchain.prompts import PromptTemplate
import json


class Routing:
    def __init__(self, qdrant_client=None):
        self.qdrant_client = qdrant_client

    
    def route(self,query: str):

        user_intent_prompt = PromptTemplate(template=user_intent_identifiction_template,input_variables=['text'])
        route_path = call_llm(input_dict={"text":query},prompt=user_intent_prompt,return_json=True)

        if route_path['route_path']=="malicious_prompt":
            return self._malicious_prompt_handler(query)
        
        if route_path['route_path'] == "conversational_chat":
            return self._converstational_chat_handler(query)

        if route_path['route_path'] == "medical_assistance":
            medical_assitance_routes = self._medical_assistance_handler(query)

            if medical_assitance_routes['route_path']=="medical_scenerio":
                return self._other_medical_scenerios(query)
            
            if medical_assitance_routes['route_path'] == "book_appointment":
                return self._book_appointment(query)


        


    def _malicious_prompt_handler(self):
        return "Prompt is Invalid"

    def _medical_assistance_handler(self,query: str):
        prompt = PromptTemplate(template=medical_assistance_tempalte,input_variables=['text'])

        response = call_llm(input_dict={"text":query},prompt=prompt,return_json=True)

        return response

    def _converstational_chat_handler(self,query: str):

        prompt = PromptTemplate(template=conversational_chat_template,input_variables=['text'])

        response = call_llm(input_dict={"text":query},prompt=prompt)

        return response        

    def _book_appointment(self,query):
        
        docs = self.qdrant_client.search_docs(query)
        prompt = PromptTemplate(template=book_appointment_template,input_variables=['text','doctors_list_speciality'])

        response = call_llm(input_dict={"text":query,"doctors_list_speciality":docs},prompt=prompt,return_json=True)

        return response


    def _other_medical_scenerios(self,query):

        prompt = PromptTemplate(template=other_medical_scenerio_template,input_variables=['text'])

        response = call_llm(input_dict={"text":query},prompt=prompt)

        return response
