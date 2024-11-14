import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Agent, Task
from crewai_tools import WebsiteSearchTool
from langchain.chat_models import ChatOpenAI
from urlbase import url

web_rag_tool = WebsiteSearchTool()

load_dotenv()

openai_model = os.getenv("OPENAI_MODEL_NAME")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("❌ OPENAI_API_KEY is not set. Please check your .env file.")
elif not openai_model:
    st.error("❌ OPENAI_MODEL_NAME is not set. Please check your .env file.")
else:
    llm = ChatOpenAI(
        model=openai_model,
        api_key=openai_api_key,
        temperature=0.2,
    )

    st.set_page_config(
    page_title="AI BLPT Yogyakarta",
    page_icon="🛠️",
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
            .stTextInput > div > div > input {
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
                background-color: #ff4b4b;
                color: #ffffff;
            }
            /* Added style for text input label */
            .stTextInput label {
                color: #000000 !important;
            }
        </style>
    """, unsafe_allow_html=True)




    st.image('https://blptjogja.or.id/wp-content/uploads/2024/07/Logo-DIY-1.png', width=50)
    st.image('https://blptjogja.or.id/wp-content/uploads/2024/07/blptjogja.png', width=400)
    
    st.title("Asisten Pelatihan BLPT Yogyakarta")

    st.markdown("""
        Selamat datang di Asisten Pelatihan BLPT Yogyakarta. 
        Silakan ajukan pertanyaan Anda di kolom di bawah ini dan kami akan membantu Anda dengan informasi yang Anda butuhkan.
    """)

    question = st.text_input("Masukkan pertanyaan Anda:", "")

    asisten_pelatihan = Agent(
        role='Asisten Pelatihan BLPT',
        goal=f'Memberikan informasi secara keseluruhan di BLPT Yogyakarta, tentang {question}',
        backstory='Asisten yang berpengetahuan luas dan berdedikasi untuk membantu pengguna menemukan program pelatihan yang tepat.',
        tools=[web_rag_tool],
        verbose=True,
        memory=True
    )

    riset_program_pelatihan = Task(
        description=(
            f'Meneliti tentang {question} di Balai Latihan Pembinaan Teknologi Yogyakarta (BLPT). '
            f"Kita akan fokus mengeksplorasi info terkini dan akurat dari {url}. Pastikan sumber informasinya valid"
        ),
        expected_output=(
            f"""
            ✨ Berikan laporan ringkas dalam bahasa indonesia yang:
            
            📝 Maksimal 3 baris per paragraf
            🎯 Fokus menjawab tentang {question}
            ❌ Katakan Maaf jika tidak ada info valid
            
            Format jawaban:
            
            💡 [Judul yang Catchy]
            
            [Paragraf 1 - max 3 baris]
            [Paragraf 2 - max 3 baris] (opsional)
            
            🔍 Sumber: [link valid]
            """
        ),
        agent=asisten_pelatihan,
        tools=[web_rag_tool]
    )
    
    search_button = st.button("Kirim")

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

            with st.spinner("🔄 Sedang mencari informasi..."):
                result = crew.kickoff()

            st.markdown(result)
