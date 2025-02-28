import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Agent, Task
from crewai_tools import WebsiteSearchTool
from langchain.chat_models import ChatOpenAI
from urlbase import url
load_dotenv()
 
openai_model = os.getenv("OPENAI_MODEL_NAME")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("❌ OPENAI_API_KEY is not set. Please check your .env file.")
elif not openai_model:
    st.error("❌ OPENAI_MODEL_NAME is not set. Please check your .env file.")
else:
    web_rag_tool = WebsiteSearchTool()
    
    llm = ChatOpenAI(
        model=openai_model,
        api_key=openai_api_key,
        temperature=0.2,
    )

    st.set_page_config(
    page_title="TSN x Gema Foundation AI",
    page_icon="🤖",
    layout="centered",
    )

    st.markdown("""
        <style>


            [data-testid="stAppViewContainer"] {
                background-color: #ffffff;
            }
            [data-testid="stHeader"] {
                background-color: #ffffff;
            }
            [data-testid="stToolbar"] {
                background-color: #ffffff;
            }
            [data-testid="stSidebar"] {
                background-color: #f8f9fa;
            }
            .stSelectbox div[data-baseweb="select"] {
                background-color: #ffffff !important;
                color: #000000 !important;
                border: 1px solid #d1d1d1 !important; /* Optional border */
            }
            .stSelectbox div[role="listbox"] {
                background-color: #ffffff !important;
                color: #000000 !important;
            }
            .stSelectbox > div > div > input {
                background-color: #ffffff;
                color: #000000 !important;
            }
            h1 {
                color: #000000 !important;
            }
            p {
                color: #000000 !important;
            }
            .stMarkdown {
                color: #000000;
            }
            .stButton button {
                background-color: #ec1856;
                color: #ffffff;
            }
            /* Added style for text input label */
            .stTextInput label {
                color: #000000 !important;
            }
            
        </style>
    """, unsafe_allow_html=True)

    st.image('tsn-gema.png', width=450)
    
    st.title("TSN x Gema Foundation AI")

    st.markdown("""
       This AI was created by Gema Foundation and collaborated with Taksina Bisnis Collage as a partner regarding technology collaboration 🇮🇩 x 🇹🇭
    """)

    question = st.text_input("Enter your question:", "")
    language = st.selectbox("Select language:", ["English 🇺🇸", "Indonesian 🇮🇩", "Thai 🇹🇭"])

    asisten_pelatihan = Agent(
        role='TSN x Gema Foundation AI',
        goal=f'Provides overall information on TSN Collage, about {question}',
        backstory='Knowledgeable and dedicated assistant to help users find information related to TSN Collage.',
        tools=[web_rag_tool],
        verbose=True,
        memory=True
    )

    riset_program_pelatihan = Task(
        description=(
            f'Researching about {question} on TSN Collage. We will focus on exploring information related to TSN Collage Takina Business Collage.'
            f"We will focus on exploring the latest and accurate information from {url}. Make sure the source of the information is valid"
        ),
        expected_output=(
            f"""
            ✨Provide a concise report in the appropriate language {language}:
            
            📝 Maximum 3 lines per paragraph
            🎯 Focus on answering about {question}
            ❌ Apologize if there is no valid information

            Answer format:

            💡 [Catchy Title]

            [Paragraph 1 - max 3 lines]
            [Paragraph 3 - max 3 lines] 
            [Paragraph 2 - max 3 lines] 

            🔍 Source: [valid link]
            """
        ),
        agent=asisten_pelatihan,
        tools=[web_rag_tool]
    )
    
    search_button = st.button("Send")

    if search_button:
        if not question:
            st.error("❌ Tolong masukkan pertanyaan Anda.")
        else:
            crew = Crew(
                agents=[asisten_pelatihan],
                tasks=[riset_program_pelatihan],
                verbose=True,
                manager_llm=llm
            )

            with st.spinner("🔄 Looking for information..."):
                result = crew.kickoff()

            st.markdown(result)
