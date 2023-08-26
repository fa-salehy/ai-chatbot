import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from langchain.document_loaders import CSVLoader
import os
import logging


# Initialize logging with the specified configuration
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.FileHandler(filename='./log/log.log'),
#         logging.StreamHandler(),
#     ],
# )
# LOGGER = logging.getLogger(__name__)
# def get_pdf_text(pdf_docs):
#     text = ""
#     for pdf in pdf_docs:
#         pdf_reader = PdfReader(pdf)
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#     return text
# Route for uploading CSV files


os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

def get_csv_text():
    text = ""
    loader = CSVLoader('./content/dataset-1.csv', encoding='utf-8')
    for row in loader.load():
        page_content = row.page_content  # Access the page_content attribute
        text += page_content + "\n"
       # Clean up the temporary file
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


# def get_vectorstore(text_chunks):
#     embeddings = OpenAIEmbeddings()
#     # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
#     vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
#     return vectorstore
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")

    if not text_chunks:
        return None  # Handle empty text_chunks

    try:
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vectorstore
    except Exception as e:
        print(f"An error occurred while creating the vectorstore: {e}")
        return None

def get_conversation_chain(vectorstore):
    if vectorstore is None:
        return None  # Handle case when vectorstore is None

    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain



def handle_userinput(user_question):
    # if "conversation" not in st.session_state or st.session_state.conversation is None:
    #     print(st.session_state.conversation)
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            # LOGGER.info(f"user asked: {user_question}.")
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    raw_text = get_csv_text()
    print("############", raw_text , "###########")
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)
    st.session_state.conversation = get_conversation_chain(vectorstore)
    
    
    st.set_page_config(page_title="Ai ChatBot",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # with st.sidebar:
    #     st.subheader("Your documents")
    #     csv_files = st.file_uploader(
    #         "Upload your CSV file(s) here and click on 'Process'", accept_multiple_files=True)
    #     if st.button("Process"):
    #         with st.spinner("Processing"):
    #             raw_text = get_csv_text(csv_files)
    #             text_chunks = get_text_chunks(raw_text)
    #             vectorstore = get_vectorstore(text_chunks)
    #             st.session_state.conversation = get_conversation_chain(vectorstore)

    st.header(":books: چت بات هوش مصنوعی")
    user_question = st.text_input("هر سوالی در زمینه بیمه دارید بپرسید:")
    if user_question:
        handle_userinput(user_question)
        
        # pdf_docs = st.file_uploader(
        #     "Upload your csv file here and click on 'Process'", accept_multiple_files=True)
        # if st.button("Process"):
        #     with st.spinner("Processing"):
        #         # get pdf text
        #         raw_text = get_pdf_text(pdf_docs)

        #         # get the text chunks
        #         text_chunks = get_text_chunks(raw_text)

        #         # create vector store
        #         vectorstore = get_vectorstore(text_chunks)

        #         # create conversation chain
        #         st.session_state.conversation = get_conversation_chain(
        #             vectorstore)

    #     csv_file_uploaded = st.file_uploader(label="Upload your CSV File here")
    #     if csv_file_uploaded is not None:
    #         def save_file_to_folder(uploadedFile):
    #             # Save uploaded file to 'content' folder.
    #             save_folder = 'content'
    #             save_path = Path(save_folder, uploadedFile.name)
    #             with open(save_path, mode='wb') as w:
    #                 w.write(uploadedFile.getvalue())

    #             if save_path.exists():
    #                 st.success(f'File {uploadedFile.name} is successfully saved!')

    #         save_file_to_folder(csv_file_uploaded)
        
    # loader = CSVLoader(file_path=os.path.join('content/', csv_file_uploaded.name))

    # vectorstore = get_vectorstore(text_chunks)

    # # create conversation chain
    # st.session_state.conversation = get_conversation_chain(
    #     vectorstore)

if __name__ == '__main__':
    main()