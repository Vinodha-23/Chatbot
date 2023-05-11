# import spacy, os
# import openai
# from django.shortcuts import render
# from dotenv import load_dotenv
# # from dummy.models import datas
# from dummy.models import chat
# from django.http import JsonResponse


# load_dotenv()
# import openai
# api_key='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'
# openai.api_key=api_key
# model_id='gpt-3.5-turbo'
# conversation=[]
# chatbot_response=""


# nlp = spacy.load("en_core_web_sm")
# response=""

# def generate_question(response, query,num_questions=1):
#     questions = []
#     for i in range(num_questions):
#         prompt = f"{query}\n{response}\nQuestion:"
#         response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=1000,
#         temperature=0.5
#         )
#         question = response.choices[0].text.strip()
#         questions.append(question)
#         return questions

# def chatbot(request):
#     chatbot_response = None
#     context = {"data": [], "response": None}
#     if api_key is not None and request.method == 'POST':
#         openai.api_key = api_key
#         firstname=request.POST.get('First_name')
#         Role=request.POST.get('Role')
#         user_input = request.POST.get('user_input')
#         prompt = user_input+Role
#         # prompt="\n".join([m['content'] for m in conversation])

#         doc = nlp(firstname)
#         person_name = None
#         for ent in doc.ents:
#             if ent.label_ == "PERSON":
#                 person_name = ent.text
#                 break
        
        
#         openai.api_key = api_key
#         conversation.append({'role':'system','content':prompt})
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             max_tokens=500,
#             messages= conversation            
#             )
#         prompt+=str(response)
    
   

           
#         # response = openai.Completion.create(
#         #     engine='gpt-3.5-turbo',
#         #     prompt=prompt,
#         #     max_tokens=1000,
#         #     temperature=0.3
           
#         # )
        
#         answer=response['choices'][0]['message']['content']
#         answer=str(answer)
#         # response_text = response["choices"][0]['text']
#         passage=answer
#         passages = answer.splitlines()
#         chatbot_response = "Hello! "
#         if person_name is not None:
#              chatbot_response += person_name + ", "+"As a "+Role
#         chatbot_response += " this context might be helpful to you "
#         for para in passages:
#             chatbot_response += "<p>" + para +"</p>"
    
#         obj=chat()
#         obj.query=user_input
#         obj.response=passage
#         obj.save()
#         results=chat.objects.all()

#         new_questions = generate_questions(response, prompt, num_questions=3)
#         context = {"data": results,"response": chatbot_response,"questions": new_questions}

#     return render(request, 'main.html', context)

import spacy, os
import openai
from django.shortcuts import render
from dotenv import load_dotenv
# from dummy.models import datas
from dummy.models import chat
from django.http import JsonResponse


load_dotenv()
import openai
api_key='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'
openai.api_key=api_key
model_id='gpt-3.5-turbo'
conversation=[]
chatbot_response=""


nlp = spacy.load("en_core_web_sm")

def generate_questions(response, related_prompt):
    questions = []
    prompt = f"{related_prompt}\n{response}\nQuestion:"
    response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1000,
            temperature=0.5
        )
    questions = response.choices[0].text.strip()
    
    return questions
    

def chatbot(request):
    related_prompt=""
    response=""
    chatbot_response = None
    context = {"data": [], "response": None}
    if api_key is not None and request.method == 'POST':
        openai.api_key = api_key
        firstname=request.POST.get('First_name')
        Role=request.POST.get('Role')
        user_input = request.POST.get('user_input')
        prompt = user_input+Role+response
       

        doc = nlp(firstname)
        person_name = None
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                person_name = ent.text
                break
        
        
        openai.api_key = api_key
        conversation.append({'role':'system','content':prompt})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=500,
            messages= conversation            
            )
        related_prompt="generate 4 questions"+str(response)
        
    

           
        # response = openai.Completion.create(
        #     engine='gpt-3.5-turbo',
        #     prompt=prompt,
        #     max_tokens=1000,
        #     temperature=0.3
           
        # )
        
        answer=response['choices'][0]['message']['content']
        answer=str(answer)
        # response_text = response["choices"][0]['text']
        passage=answer
        passages = answer.splitlines()
        chatbot_response = "Hello! "
        if person_name is not None:
             chatbot_response += person_name + ", "+"As a "+Role
        chatbot_response += " this context might be helpful to you "
        for para in passages:
            chatbot_response += "<p>" + para +"</p>"
        
        obj=chat()
        obj.query=user_input
        obj.response=passage
        obj.save()
        results=chat.objects.all()

        new_questions = generate_questions(response, related_prompt)
        context = {"data": results,"response": chatbot_response,"questions": new_questions}
        
    return render(request, 'main.html', context)