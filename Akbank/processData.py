from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Çevre değişkenlerini yükle
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


def processData():
    try:
        print(" Veri seti yükleniyor...")
        # Veri setini yükle
        loader = DirectoryLoader('./', glob='izmir veri seti.txt', loader_cls=TextLoader)
        documents = loader.load()
        print(f"✅ {len(documents)} dosya yüklendi.")
        
        print("\n Metin parçalara ayrılıyor...")
        #metni parcaladik
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["---", "\n\n", "\n"]
        )
        
        texts = text_splitter.split_documents(documents)
        print(f" {len(texts)} parçaya ayrıldı.")
        
        print("\nEmbedding modeli yükleniyor...")
        # Google'ın ücretsiz embedding modelini kullan
        embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        print(" Embedding modeli hazır.")
        
        print("\nVektör veritabanı oluşturuluyor...")
        # Vektörleri ChromaDB'ye kaydet
        vectordb = Chroma.from_documents(
            documents=texts,
            embedding=embedding_model,
            persist_directory="./chroma_db"
        )
        print(" Vektör veritabanı başarıyla oluşturuldu!")
        print(f" Konum: ./chroma_db")
        
    except FileNotFoundError:
        print("HATA: 'izmir veri seti.txt' dosyası bulunamadı!")
        print("Lütfen dosyanın proje klasöründe olduğundan emin olun.")
    except Exception as e:
        print(f" HATA: {str(e)}")


if __name__ == "__main__":
    print("=" * 50)
    print("İZMİR ROTA ASİSTANI - VERİ İŞLEME")
    print("=" * 50)
    processData()