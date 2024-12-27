import os
import json
import pandas as pd
import traceback
import pandas as pd
from dotenv import load_dotenv,find_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging

# importnat libraries
from langchain_ai21.chat_models import ChatAI21
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import json
import PyPDF2




load_dotenv()
api_key=os.getenv("AI21_API_KEY")



llm=ChatAI21(api_key=api_key,model="jamba-instruct",temprature=0.7,max_tokens=50000)

prompt=PromptTemplate.from_template("""
                             Text:{text}
                             you are an expert mcq maker.given the above text, it is your job to \
                             create a quiz of {number} multiple choice question for {subject} students in {tone} tone. \
                             make sure the question are not repeated and check all the questions to be confirming the text as well. \
                             make sure to format your response like RESPONSE_JSON below and use it as a guide. \
                             ensure to make {number} mcqs
                             ### RESPONSE_JSON
                             {response_json}""")

chain=LLMChain(llm=llm,prompt=prompt,output_key="quiz",verbose=True)



template2=PromptTemplate.from_template("""
                                       
          you are an expert english grammarian and writer.given a multiple choice quiz for {subject} students. \
          you need to evaluate the complexity of the question and give a complete analysis of the quiz. only at max 50 words for complexity. \
          if the quiz is not at per the cognitive and analytical abilities of the students, \
              update the quiz question which need to be changed the tone such that it perfectly fitsthe student abilities \
              
              Quiz_MCQS:
              {quiz}
              
              check from an expert english writer of the above quiz   \                         
                                       """)


review_chain=LLMChain(llm=llm,prompt=template2,output_key="review",verbose=True)


generate_evaluate_chain=SequentialChain(
    chains=[chain,review_chain],
    input_variables=["text","number","subject","tone","response_json"],
    output_variables=["quiz","review"],
    verbose=True
)




