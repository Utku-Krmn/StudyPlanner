# Study Planner API

FastAPI, SQLite, SQLAlchemy, Pydantic, JWT ve React/TypeScript kullanılarak hazırlanmış bir öğrenci çalışma planlayıcısıdır.

## Özellikler

- Kullanıcı kayıt, giriş ve profil bilgisi
- JWT Bearer token ile korunan endpoint'ler
- Ders ekleme, listeleme, güncelleme ve silme
- Görev/ödev ekleme, filtreleme, güncelleme, tamamlama ve silme
- Sınav ekleme, listeleme, güncelleme ve silme
- Önümüzdeki 7 günün görev/sınavları ve tamamlanan görevleri gösteren dashboard
- Her kullanıcının yalnızca kendi verilerine erişebilmesi
- Swagger UI ile interaktif API testi

## VS Code ile çalıştırma

VS Code'da `StudyPlanner` klasörünü açın. Ardından Terminal > New Terminal seçeneğini kullanıp şu komutları sırayla çalıştırın:

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows kullanıyorsanız aktivasyon komutu:

```powershell
.venv\Scripts\activate
```

Sunucu başladıktan sonra:

- Web arayüzü: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Sağlık kontrolü: http://127.0.0.1:8000/health

## Swagger ile test sırası

1. `POST /auth/register` ile kayıt olun.
2. Sayfanın üstündeki **Authorize** düğmesine basın.
3. `username` alanına kullanıcı adınızı, `password` alanına kayıt olurken belirlediğiniz şifreyi girin. Diğer alanları boş bırakıp **Authorize** düğmesine basın.
4. Önce `POST /courses`, sonra görev ve sınav endpoint'lerini deneyin.
5. `GET /dashboard` ile özet bilgileri görüntüleyin.

## Örnek veriler

Kayıt:

```json
{
  "name": "Ayşe Yılmaz",
  "username": "ayseyilmaz",
  "email": "ayse@example.com",
  "password": "123456"
}
```

Ders:

```json
{
  "name": "Matematik",
  "code": "MAT101",
  "description": "Temel matematik dersi"
}
```

Görev (önce oluşturulan dersin `id` değerini kullanın):

```json
{
  "title": "Problem setini tamamla",
  "description": "1-20 arası sorular",
  "due_date": "2026-11-25",
  "course_id": 1
}
```

Sınav:

```json
{
  "title": "Matematik Vize",
  "exam_date": "2026-11-27T10:00:00",
  "location": "A101",
  "notes": "İlk 5 ünite",
  "course_id": 1
}
```

## Proje yapısı

```text
StudyPlanner/
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── courses.py
│   │   ├── dashboard.py
│   │   ├── exams.py
│   │   └── tasks.py
│   ├── auth.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

SQLite veritabanı (`study_planner.db`) uygulama ilk çalıştığında otomatik oluşur.

## Frontend geliştirme

Frontend kaynakları `frontend/src` klasöründedir. Arayüzde değişiklik yaptıktan sonra üretim dosyalarını yeniden oluşturmak için:

```bash
cd frontend
npm install
npm run build
```

Normal kullanımda ayrıca bir frontend sunucusu çalıştırmanız gerekmez; FastAPI derlenmiş React arayüzünü otomatik sunar.
