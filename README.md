# Tech Agent

Bu projenin ne yaptığı ve kimin için olduğu hakkında kısa bir açıklama


This project is a web application developed for the BTK Hackathon Eğitim. It consists of a frontend built with React and a backend powered by FastAPI.

## Proje Yetenekleri

Bu proje, öğrenme deneyimlerini geliştirmek için yapay zekadan yararlanarak eğitimi desteklemektedir. Yapay zeka özellikleri şunları içerir:

-  **Soru Çözme**: Sistem çok çeşitli soruları çözebilir ve ayrıntılı çözümler sağlayabilir.
-  **Soru Üretimi**: Kullanıcıların pratik yapmalarına ve bilgilerini test etmelerine yardımcı olmak için yeni sorular oluşturabilir.

- **Video Açıklamaları**: Yapay zeka, çözümleri video aracılığıyla açıklayarak materyalin daha ilgi çekici ve kapsamlı bir şekilde anlaşılmasını sağlayabilir.

- **Ders Notu Açıklamaları**: Ders notlarınızı veya kitaplarınızı pdf formatında yükleyerek podcast tarzında dinleyebilirsiniz.

  
## Özellikler

- Çoklu Dil Desteği
- Canlı Ön İzleme
- Tam Ekran Modu
- Tüm Platformlara Destek
- Tüm Soru Tiplerini Destekler
- Video Şeklinde Sunum
- Podcast


## Proje Yapısı
- **Frontend**: `frontend` dizininde bulunan bu proje bölümü, Create React App ile başlatılmış bir React uygulamasıdır.
- **Backend**: `backend` dizininde bulunan bu proje bölümü, bir FastAPI uygulamasıdır.

## Gereksinimler

- Node.js ve npm (frontend için)
- Python 3.x ve pip (backend için)

## Kurulum Talimatları

### Frontend

1. `frontend` dizinine gidin:
   ```bash
   cd frontend
   ```

2. Bağımlılıkları yükleyin:
   ```bash
   npm install
   ```

3. Geliştirme sunucusunu başlatın:
   ```bash
   npm start
   ```

   Tarayıcınızda görüntülemek için [http://localhost:3000](http://localhost:3000) adresini açın.

### Backend

1. `backend` dizinine gidin:
   ```bash
   cd backend
   ```

2. Bir sanal ortam oluşturun:
   ```bash
   python -m venv venv
   ```

3. Sanal ortamı etkinleştirin:

   - Windows'ta:
     ```bash
     venv\Scripts\activate
     ```

   - macOS ve Linux'ta:
     ```bash
     source venv/bin/activate
     ```

4. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

5. FastAPI uygulamasını çalıştırın:
   ```bash
   uvicorn main:app --reload
   ```

   API'ye erişmek için [http://localhost:8000](http://localhost:8000) adresini açın.

## Kullanılabilir Komutlar

### Frontend

- `npm start`: Uygulamayı geliştirme modunda çalıştırır.
- `npm test`: Test çalıştırıcısını başlatır.
- `npm run build`: Uygulamayı üretim için derler.
- `npm run eject`: Uygulamayı Create React App'den çıkarır.

### Backend

- `uvicorn main:app --reload`: FastAPI sunucusunu geliştirme modunda başlatır.

## Daha Fazla Bilgi Edinin

- [Create React App belgeleri](https://facebook.github.io/create-react-app/docs/getting-started)
- [React belgeleri](https://reactjs.org/)
- [FastAPI belgeleri](https://fastapi.tiangolo.com/)

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.
