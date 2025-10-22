import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import sqlite3
import bcrypt
import os


load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Sayfa yapisi
st.set_page_config(
    page_title="İzmir Rota Asistanı",
    page_icon="🏛️",
    layout="wide"
)


def initialize_db():
    """Kullanıcı veritabanını oluşturur"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT)''')
    conn.commit()
    conn.close()


def addUser(userName, password):
    """Yeni kullanıcı ekler"""
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (userName, hashedPassword))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Kullanıcı zaten var
    finally:
        conn.close()


def verifyUser(userName, password):
    """Kullanıcı girişini doğrular"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (userName,))
    result = c.fetchone()
    conn.close()
    if result:
        return bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8'))
    else:
        return False  # Kullanıcı bulunamadı


# Veritabanını başlat
initialize_db()

# Session state başlat
if "loggined_in" not in st.session_state:
    st.session_state.loggined_in = False
    st.session_state.username = None

# giris
if not st.session_state.loggined_in:
    st.sidebar.title("Giriş Yap / Kayıt Ol")
    selection = st.sidebar.radio("Seçim Yapın", ["Giriş Yap", "Kayıt Ol"])

    if selection == "Giriş Yap":
        with st.sidebar.form("login_form"):
            userName = st.text_input("Kullanıcı Adı")
            password = st.text_input("Şifre", type="password")
            submitted = st.form_submit_button("Giriş Yap")

            if submitted:
                if verifyUser(userName, password):
                    st.session_state.loggined_in = True
                    st.session_state.username = userName
                    st.success("Giriş başarılı!")
                    st.rerun()
                else:
                    st.error("Kullanıcı adı veya şifre yanlış.")
                    
    elif selection == "Kayıt Ol":
        with st.sidebar.form("register_form"):
            newUserName = st.text_input("Kullanıcı Adı")
            newPassword = st.text_input("Şifre", type="password")
            submitted = st.form_submit_button("Kayıt Ol")

            if submitted:
                if addUser(newUserName, newPassword):
                    st.success("Kayıt başarılı! Giriş yapabilirsiniz.")
                else:
                    st.error("Bu kullanıcı adı zaten alınmış. Başka bir tane deneyin.")

# ana sayfa
else:
    st.title("🏛️ İzmir Rota Asistanı")
    st.markdown("*İzmir'de gezilecek yerleri keşfedin ve kişiselleştirilmiş rotalar oluşturun!*")

    # RAG bileşenlerini yükle
    @st.cache_resource
    def load_components():
        """Vektör veritabanı ve LLM modelini yükler"""
        try:
            # Embedding modelini yükle
            embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            
            # Vektör veritabanını yükle
            vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)

            # Gemini LLM modelini yükle
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.7,
                convert_system_message_to_human=True
            )

            # Custom prompt template
            prompt_template = """Sen İzmir'de yerel bir turist rehberisin. İzmir'deki gezilecek yerler, 
            restoranlar, tarihi mekanlar ve aktiviteler hakkında detaylı bilgiye sahipsin.
            
            Verilen bilgilere dayanarak kullanıcının sorusunu yanıtla. Eğer bilmiyorsan, bilmediğini söyle.
            Yanıtlarını Türkçe, dostça ve yardımsever bir tonda ver.
            
            Bağlam: {context}
            
            Soru: {question}
            
            Cevap:"""
            
            PROMPT = PromptTemplate(
                template=prompt_template, 
                input_variables=["context", "question"]
            )

            # RAG zincirini kur
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
                chain_type="stuff",
                chain_type_kwargs={"prompt": PROMPT},
                return_source_documents=True
            )

            return qa_chain
        
        except Exception as e:
            st.error(f"Model yüklenirken hata oluştu: {str(e)}")
            st.info(" Lütfen önce 'processData.py' dosyasını çalıştırarak vektör veritabanını oluşturun.")
            return None

    # Bileşenleri yükle
    qa_chain = load_components()

    if qa_chain is None:
        st.stop()

    # Hoş geldin mesajı
    st.info(" Merhaba! İzmir'de bugün ne yapmak istersin?")

    # Kategori butonları
    st.markdown("### Hızlı Kategoriler")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏛️ Tarihi Yerler", use_container_width=True):
            st.session_state.current_query = "İzmir'deki tarihi yerler nelerdir? Birkaçını listeler misin?"
            
        if st.button("🎨 Müze ve Sanat", use_container_width=True):
            st.session_state.current_query = "İzmir'deki sanat galerileri ve müzeler nelerdir?"

    with col2:
        if st.button("🌊 Doğal Güzellikler", use_container_width=True):
            st.session_state.current_query = "İzmir'deki doğal güzellikler hakkında bilgi verip bir rota oluşturur musun?"
            
        if st.button("🎉 Eğlence Mekanları", use_container_width=True):
            st.session_state.current_query = "İzmir'de keyifli ve eğlenceli bir zaman geçirmek için neler yapılır?"

    with col3:
        if st.button("🍽️ Yeme-İçme", use_container_width=True):
            st.session_state.current_query = "İzmir'in meşhur yeme-içme mekanları hakkında bilgi verir misin?"
            
        if st.button("🛍️ Alışveriş", use_container_width=True):
            st.session_state.current_query = "İzmir'deki alışveriş merkezleri nerelerdir?"

    # Özel rota oluşturma
    st.markdown("---")
    st.markdown("### ✨ Bana Özel Bir Rota Oluştur")
    
    with st.form("route_form"):
        user_query = st.text_area(
            "Neler yapmak istediğini, nerede ve kiminle yapmak istediğini yazabilirsin.",
            placeholder="Örnek: Ailemle birlikte İzmir'de tarihi yerleri gezmek ve deniz kenarında yemek yemek istiyorum."
        )
        submitted = st.form_submit_button("Rota Oluştur", use_container_width=True)

        if submitted and user_query.strip():
            st.session_state.current_query = user_query

    # Yanıt oluşturma ve gösterme
    if "current_query" in st.session_state and st.session_state.current_query:
        with st.spinner("Düşünüyorum..."):
            try:
                result = qa_chain.invoke({"query": st.session_state.current_query})
                response = result["result"]
                
                # Sonucu göster
                st.markdown("---")
                st.markdown("### Yanıt")
                st.markdown(f"**Soru:** {st.session_state.current_query}")
                st.markdown(f"İzmir Rota Asistanı: {response}")
                
                # Query'yi temizle
                st.session_state.current_query = None
                
            except Exception as e:
                st.error(f" Bir hata oluştu: {str(e)}")

    # Sidebar - Kullanıcı bilgisi
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"###  Hoşgeldin!")
    st.sidebar.markdown(f"**{st.session_state.username}**")
    
    if st.sidebar.button("🚪 Çıkış Yap", use_container_width=True):
        st.session_state.loggined_in = False
        st.session_state.username = None
        if "current_query" in st.session_state:
            del st.session_state.current_query
        st.rerun()