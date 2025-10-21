                ızmir rota asistanı
İzmir'de gezilecek yerleri keşfetmenize ve kişiselleştirilmiş rotalar oluşturmanıza yardımcı olan yapay zeka destekli turist rehberi.

                Amaç
Bu proje, İzmir'i ziyaret eden veya İzmir'de yaşayan kişilerin şehri daha iyi keşfetmelerine yardımcı olmak amacıyla geliştirilmiştir. RAG (Retrieval Augmented Generation) teknolojisi kullanılarak, kullanıcıların sorularına İzmir veri setinden alınan bilgilerle yanıtlar verilmektedir.

                Temel Özellikler
RAG Tabanlı Chatbot: Gemini API ile güçlendirilmiş akıllı sohbet sistemi
Hızlı Kategoriler: Tarihi yerler, müzeler, doğal güzellikler ve daha fazlası
Kişiselleştirilmiş Rotalar: İhtiyaçlarınıza göre özel rota önerileri

                Veri Seti Hakkında
Veri Kaynağı
Projede kullanılan "izmir veri seti.txt" dosyası, İzmir'deki turistik yerler, restoranlar, müzeler, tarihi mekanlar ve aktiviteler bilgiler içermektedir.Veri seti manuel olarak oluşturuldu.İçeriği:
Tarihi ve kültürel mekanlar, Müzeler ve sanat galerileri, Doğal güzellikler ve parklar, Yeme-içme mekanları, Alışveriş merkezleri, Eğlence ve aktivite alanları.

Veri İşleme:
Veri seti, RAG pipeline'ında kullanılmak üzere şu adımlarla işlenmektedir:
Metin Yükleme: DirectoryLoader ile txt dosyası okunur
Chunking: RecursiveCharacterTextSplitter ile 1000 karakterlik parçalara bölünür (200 karakter örtüşme ile)
Vektörleştirme: Google Embedding-001 modeli ile vektörlere dönüştürülür
Depolama: ChromaDB vektör veritabanında saklanır

                Kullanılan Teknolojiler
RAG Pipeline
Framework: LangChain
Generation Model: Google Gemini Pro
Embedding Model: Google Embedding
Vector Database: ChromaDB
Retrieval Method: Similarity Search 
-Web Arayüzü:
Framework: Streamlit
Veritabanı: SQLite3
Güvenlik: bcrypt (şifre hashleme)

                RAG Pipeline Akışı
[Kullanıcı Sorusu]
        ↓
[Embedding Modeli] → Soruyu vektöre dönüştür
        ↓
[ChromaDB] → En benzer 3 dökümanı bul
        ↓
[Context + Soru] → Gemini Pro'ya gönder
        ↓
[Gemini Pro] → Yanıt oluştur
        ↓
[Kullanıcıya Yanıt]

Sistem Bileşenleri

                Veri İşleme Katmanı (processData.py)

-Veri yükleme ve temizleme
Metin parçalama (chunking)
Embedding oluşturma
Vektör veritabanına kaydetme
-Backend Katmanı (frontend.py)
Kullanıcı kimlik doğrulama
RAG pipeline yönetimi
Prompt engineering
Yanıt oluşturma
-Frontend Katmanı (Streamlit UI)
Kullanıcı arayüzü
Chat interface
Session management

                Kurulum ve Çalıştırma:

-Gereksinimler
Python 3.8 veya üzeri
Google Gemini API Key 

-Adım 1: Projeyi Klonlayın
git clone https://github.com/kullaniciadi/izmir-rota-asistani.git
cd Akbank

-Adım 2: Virtual Environment Oluşturun:
python3 -m venv venv
source venv/bin/activate

-Adım 3: Gerekli Paketleri Yükleyin
pip install -r requirements.txt

-Adım 4: API Key Ayarlayın: Google AI Studio adresinden ücretsiz API key alın. Proje klasöründe .env dosyası oluşturun:
GOOGLE_API_KEY=your_api_key_here

-Adım 5: Vektör Veritabanını Oluşturun
python processData.py

-Adım 6: Web Uygulamasını Başlatın: Tarayıcınızda otomatik olarak http://localhost:8501 açılacaktır.
streamlit run frontend.py


                Kullanım Kılavuzu
1. Kayıt ve Giriş
Sol menüden "Kayıt Ol" seçeneğini seçin
Kullanıcı adı ve şifre belirleyin
"Giriş Yap" ile sisteme giriş yapın

2. Hızlı Kategoriler
Ana sayfadaki butonlarla hızlıca öneri alın:
🏛️ Tarihi Yerler: Kültür Park, Kadifekale vb.
🎨 Müzeler: Arkeoloji Müzesi, Etnografya Müzesi
🌊 Doğal Güzellikler: Kordon, İnciraltı
🎉 Eğlence: Lunapark, sinema, konser mekanları
🍽️ Yeme-İçme: Meşhur İzmir lokantaları
🛍️ Alışveriş: AVM'ler ve çarşılar

3. Özel Rota Oluşturma
Aşağıdaki metin kutusuna rota isteğinizi yazın


                Elde Edilen Sonuçlar
Başarılar 
RAG pipeline başarıyla çalışıyor
Gemini Pro ile Türkçe yanıtlar mükemmel
Responsive ve kullanıcı dostu arayüz

Karşılaşılan Zorluklar
Veri seti sınırlı olduğunda yanıtlar genel kalabiliyor
Chunking parametrelerinin optimizasyonu
Prompt engineering ile yanıt kalitesini artırma

Gelecek İyileştirmeler
Daha geniş veri seti
Görsel içerik desteği (harita, fotoğraflar)
Çoklu dil desteği
Kullanıcı favori rotaları