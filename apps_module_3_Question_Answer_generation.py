import streamlit as st
#from transformers import pipeline

#https://stackoverflow.com/questions/56611698/pandas-how-to-read-csv-file-from-google-drive-public
#https://stackoverflow.com/questions/18885175/read-a-zipped-file-as-a-pandas-dataframe 

import pandas as pd
url='https://drive.google.com/file/d/1eta741E5t6Kf-5y_LpNjREXt5y7k6v84/view?usp=sharing'

df = pd.read_csv('https://drive.usercontent.google.com/download?id={}&export=download&authuser=0&confirm=t'.format(url.split('/')[-2]), sep='##', names=['text', 'key', 'period' , 'title'])

import os

from transformers import pipeline

import pandas as pd

import spacy



opts = df['key'].tolist()
opts_c = []

for op in opts:
    if op not in opts_c:
        opts_c.append(op)

opts = opts_c 

st.set_page_config(
    page_title="Text Generation App", page_icon=":pencil2:", layout="wide"
)

# Add a title and a description
st.title("Module_3_Question_Generation")
st.write(
    "This application generates question answer based on the topic choosen on the author's text of interest."
)

# Initialize the Hugging Face model
#generator = pipeline("text-generation", model="gpt2")

# Create a sidebar for input parameters
st.sidebar.title("Input Options")
input_text = st.sidebar.text_input("Select options")
option = st.sidebar.selectbox(
    "Select topic of interest?",
    opts,
)

generate_button = st.sidebar.button("Generate")

if generate_button:

    #hf_token ="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"

    #os.environ["HUGGINGFACEHUB_API_TOKEN"]= hf_token # replace hf_token with your HuggingFace API-token 
                
    df1 = df.loc[df['key'] == option]

    print(df1)

    hi = df1['text'].tolist()           



    arts = ''
    c_l = []
    collected = []


    for h in hi:
            cf1 = str(h).count(option)
            cf2 = str(h).count(str(option).lower())
            cf3 = cf1 + cf2
            if cf3 > 0:
                
        
                arts += h + '\n'
                c_l.append(h)


    # Set page title and description

    # Create a button to generate text


    # Generate and display text when the button is clicked
    try:
        os.remove('modul1_inter1.txt')
    except:
        pass
    try:
        os.remove('modul1_inter2.txt')
    except:
        pass

    try:
        os.remove('generated_summary_module36.txt')
    except:
        pass


        

    import time

    m_str = ''
    C = 0
    main_res = ''

    for c in c_l:

        if len(m_str) < 8000:
            m_str += c
            C = 0

        if len(c) > 8000:
            
            #print(len(m_str))
            ny1 = open('modul1_inter1.txt', 'a+')
            ny1.write(str(c) + '\n')
            ny1.close()
            print('here')
            C = 2 
            m_str = ''
        
        if len (m_str) > 8000:
            
            #print(len(m_str))
            ny1 = open('modul1_inter2.txt', 'a+')
            ny1.write(str(m_str) + '\n')
            ny1.close()
            print('here')
            C = 1 
            m_str = ''

        
        
        if C == 1:
        
            from langchain.document_loaders import TextLoader
            loader = TextLoader('modul1_inter2.txt')
            documents = loader.load()
            
            import textwrap
            
            def wrap_text_preserve_newlines(text, width=110):
                # Split the input text into lines based on newline characters
                lines = text.split('\n')
            
                # Wrap each line print(wrap_text_preserve_newlines(str(documents[0])))
                wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
            
                # Join the wrapped lines back together using newline characters
                wrapped_text = '\n'.join(wrapped_lines)
            
                return wrapped_text
            
            from langchain.text_splitter import CharacterTextSplitter
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.split_documents(documents)
            
            # Embeddings
            from langchain.embeddings import HuggingFaceEmbeddings
            embeddings = HuggingFaceEmbeddings()
            from langchain.vectorstores import FAISS
            db = FAISS.from_documents(docs, embeddings)
            query = option
            docs = db.similarity_search(query)
            
            from langchain.chains.question_answering import load_qa_chain
            from langchain import HuggingFaceHub
            from langchain.output_parsers.regex import RegexParser
            
            hf_token2 ="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"
            import os
        
            os.environ["HUGGINGFACEHUB_API_TOKEN"]= hf_token2 # replace hf_token with your HuggingFace API-token 
        
            #llm=HuggingFaceHub(repo_id="togethercomputer/RedPajama-INCITE-Chat-3B-v1", model_kwargs={"temperature":0.8, "max_length":512})
            llm=HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs={"temperature":0.8, "max_new_tokens":1028})
            
            from langchain.prompts import PromptTemplate
            #Generate a questions the topic marriage for which answers can be found strictly in the given passage below
        
            prompt = PromptTemplate.from_template(
                """
                Generate questions and answers on the topic """+str(option)+""" for which answers can be found strictly in the given passage below
                
                {context}
                
                
                
                Helpful Answer:
                """)
            
            
            
            #documents = 'But let us see in what sense Marriage is honorable in all and the bed undefiled. Because  it preserves the believer in chastity. Here he also alludes to the Jews, because they accounted the woman after childbirth polluted: and whosoever comes from the bed, it is said, is not clean. Those things are not polluted which arise from nature, O ungrateful and senseless Jew, but those which arise from choice. For if marriage is honorable and pure, why forsooth dost thou think that one is even polluted by it?'
            query = ""
            
            
            chain = load_qa_chain(llm, chain_type="stuff", 
                prompt=prompt,
                # this is the default values and can be modified/omitted
                document_variable_name="context",)
            
            reps = chain.run({"input_documents": docs, "question": query})
            #print('1')
            #print(reps)
            #time.sleep(10000)
            
            

            dv = str(reps).split('Helpful Answer:')
            tgh = str(dv[-1]).split('\n')
            

            for th in tgh:
                bkl = open('generated_summary_module36.txt', 'a+')
                bkl.write(str(th).strip() + '\n')
                bkl.close()
            C = 0
            os.remove('modul1_inter2.txt')



        if C == 2:
        
            from langchain.document_loaders import TextLoader
            loader = TextLoader('modul1_inter1.txt')
            documents = loader.load()
            
            import textwrap
            
            def wrap_text_preserve_newlines(text, width=110):
                # Split the input text into lines based on newline characters
                lines = text.split('\n')
            
                # Wrap each line print(wrap_text_preserve_newlines(str(documents[0])))
                wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
            
                # Join the wrapped lines back together using newline characters
                wrapped_text = '\n'.join(wrapped_lines)
            
                return wrapped_text
            
            from langchain.text_splitter import CharacterTextSplitter
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.split_documents(documents)
            
            # Embeddings
            from langchain.embeddings import HuggingFaceEmbeddings
            embeddings = HuggingFaceEmbeddings()
            from langchain.vectorstores import FAISS
            db = FAISS.from_documents(docs, embeddings)
            query = option
            docs = db.similarity_search(query)
            
            from langchain.chains.question_answering import load_qa_chain
            from langchain import HuggingFaceHub
            from langchain.output_parsers.regex import RegexParser
            
            hf_token2 ="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"
            os.environ["HUGGINGFACEHUB_API_TOKEN"]= hf_token2 # replace hf_token with your HuggingFace API-token 
        
            #llm=HuggingFaceHub(repo_id="togethercomputer/RedPajama-INCITE-Chat-3B-v1", model_kwargs={"temperature":0.8, "max_length":512})
            llm=HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs={"temperature":0.8, "max_new_tokens":1028})
            
            from langchain.prompts import PromptTemplate
            #Generate a questions the topic marriage for which answers can be found strictly in the given passage below
            
            prompt = PromptTemplate.from_template(
                """
                Generate questions and answers on the topic """+str(option)+""" for which answers can be found strictly in the given passage below
                
                {context}
                
                
                
                Helpful Answer:
                """)
            
            
            
            #documents = 'But let us see in what sense Marriage is honorable in all and the bed undefiled. Because  it preserves the believer in chastity. Here he also alludes to the Jews, because they accounted the woman after childbirth polluted: and whosoever comes from the bed, it is said, is not clean. Those things are not polluted which arise from nature, O ungrateful and senseless Jew, but those which arise from choice. For if marriage is honorable and pure, why forsooth dost thou think that one is even polluted by it?'
            query = ""
            
            
            chain = load_qa_chain(llm, chain_type="stuff", 
                prompt=prompt,
                # this is the default values and can be modified/omitted
                document_variable_name="context",)
            
            reps = chain.run({"input_documents": docs, "question": query})
            #print(reps)
            #time.sleep(10000)

            dv = str(reps).split('Helpful Answer:')
            tgh = str(dv[-1]).split('\n')
            
            

            for th in tgh:
                bkl = open('generated_summary_module36.txt', 'a+')
                bkl.write(str(th).strip() + '\n')
                bkl.close()
            os.remove('modul1_inter1.txt')




    tio = open('generated_summary_module36.txt', 'r')
    output_text  = tio.readlines()
    tio.close()

    for th in output_text:
        main_res += str(th) 
                



    


            
            
        
    
            
        
if generate_button:
    with st.spinner("Generating text..."):
        output_text_real = main_res
    st.subheader("Generated Text:")
    st.write(output_text_real)