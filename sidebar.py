import streamlit as st
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":1, "max_length":512})
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectorstore.as_retriever(), memory= memory)
    return conversation_chain

visited_urls = set()
unique_content_list = []
def crawl_and_return_text(url):
    # Check if the URL has been visited
    if url in visited_urls:
        return ""

    print(f"Visiting: {url}")

    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Extract information or perform actions based on your needs
        # In this example, we store the paragraphs and headings of each page in a list
        content = extract_text_content(soup)
        
        # Check if the content is unique before storing
        if content and content not in unique_content_list:
            unique_content_list.append(content)
        
        # Mark the URL as visited
        visited_urls.add(url)

        # Extract links and crawl them recursively
        host = urlparse(url).scheme + "://" + urlparse(url).hostname
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href:
                full_url = urljoin(url, href)

                # Check if the link points to the same part of the same page
                if urldefrag(full_url).url == urldefrag(url).url:
                    continue

                if full_url.startswith(host):
                    content += crawl_and_return_text(full_url)

        return content

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return ""

def extract_text_content(soup):
    # Extract paragraphs and headings from the page while maintaining their order
    content_elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table','ul', 'div'])
    content = '\n'.join(element.get_text() for element in content_elements)
    return content
    
def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        
def main():
    load_dotenv()
    
    st.set_page_config(page_title="Web Magic", page_icon=":magic_wand:")
    
    st.write(css, unsafe_allow_html=True)
    
    if"conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    
    st.header(" :magic_wand: Web Magic : Ask The Web ")
    with st.sidebar:
        st.subheader(":one: Process your website first !")
        web_url = st.text_input("Enter Full URL of Your Website", placeholder="Enter full URL !")
    
        if st.button("Process"):
            with st.spinner("Processing"):
                content = crawl_and_return_text(web_url)
                st.sidebar.write(content)
                text_chunks = get_text_chunks(content)
                # create vector store with embeddings
                vectorstore = get_vectorstore(text_chunks)
                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)
            
    user_question = st.text_input(":two: Ask a question about your website now : ", placeholder="Process the website first !")
    if user_question:
        handle_userinput(user_question)

if __name__ == '__main__':
    main()