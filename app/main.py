
from fastapi import FastAPI
from settings import engine
from routers import category, auth, user
import models


app = FastAPI()


# FastAPI'de migration işlemini gerçekleştirmek için django'da olduğu gibi ekstra bir ifade kullanmıyoruz.
# Tek yapmamız gereken terminalde 'main.py' dosyasının bulunduğu dizine geçerek 'uvicorn main:app --reload' powershell kodunu çalıştırmaktır.
# Aşağıda ki söz dizimi ise model içerisinde ki sınıfları göçe hazırlamak için kullanılmaktadır.
models.Base.metadata.create_all(bind=engine)


# router klasörü altında açtığımız .py uzantılı dosyaları buraya register ediyoruz ki proje ayağı kaldırılırken ilgili dosyalara yazılmış fonksiyonlar devreye girsin
app.include_router(category.router)
app.include_router(auth.router)
app.include_router(user.router)


