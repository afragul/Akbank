Projeniz için hazırladığım kapsamlı ve profesyonel `README.md` dosyası aşağıdadır. Bu taslak, paylaştığınız `frontend.py`, `processData.py` ve mevcut `README.md` dosyalarındaki teknik detaylara dayanarak oluşturulmuştur:

---

# 🏛️ İzmir Rota Asistanı

İzmir'i keşfetmek isteyen ziyaretçiler ve yerel halk için geliştirilmiş, **Yapay Zeka (RAG - Retrieval Augmented Generation)** destekli bir akıllı turist rehberidir. Bu uygulama, kullanıcılara İzmir'in tarihi mekanlarından yeme-içme noktalarına kadar geniş bir yelpazede kişiselleştirilmiş rota önerileri sunar.

## 🎯 Amaç

Proje, İzmir'e dair özel olarak hazırlanmış bir veri setini kullanarak, kullanıcıların sorularına (Gemini API aracılığıyla) doğru, güncel ve bağlama uygun yanıtlar vermeyi hedefler.

## ✨ Temel Özellikler

* **Akıllı Sohbet Sistemi:** Gemini Pro ve RAG teknolojisi ile İzmir özelinde bilgilendirme.
* **Hızlı Kategoriler:** Tek tıkla Tarihi Yerler, Müzeler, Doğal Güzellikler, Eğlence, Yeme-İçme ve Alışveriş önerileri.
* **Kişiselleştirilmiş Rotalar:** Kullanıcının özel isteklerine (örn: "Ailemle deniz kenarında yemek") göre özelleşmiş gezi planları.
* **Güvenli Kullanıcı Yönetimi:** SQLite3 ve `bcrypt` şifreleme altyapılı kayıt ve giriş sistemi.

## 🛠️ Kullanılan Teknolojiler

### **Backend & AI (RAG Pipeline)**

* **Framework:** LangChain
* **LLM:** Google Gemini Pro (`gemini-1.5-flash`)
* **Embedding:** Google Embedding-001
* **Vektör Veritabanı:** ChromaDB

### **Frontend & Database**

* **Web Arayüzü:** Streamlit
* **Veritabanı:** SQLite3 (Kullanıcı verileri için)
* **Güvenlik:** Bcrypt (Şifre hashleme)

## 🚀 Kurulum ve Çalıştırma

### 1. Gereksinimler

* Python 3.8+
* Google Gemini API Key

### 2. Adımlar

```bash
# Projeyi klonlayın
git clone https://github.com/afragul/Akbank.git
cd Akbank

# Sanal ortam oluşturun ve aktif edin
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

```

### 3. API Anahtarını Ayarlayın

Proje ana dizininde bir `.env` dosyası oluşturun ve API anahtarınızı ekleyin:

```env
GOOGLE_API_KEY=kendi_api_anahtariniz

```

### 4. Veriyi İşleyin (Vektör Veritabanı Oluşturma)

Uygulamayı ilk kez çalıştırmadan önce `izmir veri seti.txt` dosyasını vektör veritabanına dönüştürmeniz gerekir:

```bash
python processData.py

```

### 5. Uygulamayı Başlatın

```bash
streamlit run frontend.py

```

## 📂 Dosya Yapısı

* `frontend.py`: Streamlit arayüzü, kullanıcı yönetimi ve RAG zincirinin kurulduğu ana dosya.
* `processData.py`: Veri setinin yüklenmesi, parçalanması (chunking) ve ChromaDB'ye kaydedilmesi işlemlerini yapar.
* `requirements.txt`: Proje bağımlılıklarını içerir.
* `izmir veri seti.txt`: İzmir'deki turistik yerler ve mekanlar hakkında manuel oluşturulmuş veri seti.

---
Streamlit linki: https://izmir-rota-rehberi.streamlit.app/
