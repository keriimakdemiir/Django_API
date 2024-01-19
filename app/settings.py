
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# veri tabanının lokasyonunu yani yolunu (dir) bir değişkene atıyoruz.
SQLALCEMY_DATABASE_URL = 'sqlite:///./api.db'

# SQLALCEMY ORM aracını kullana  bir web application yani bizim api'miz ile veri tabanının nasıl konuşacağını ayarladığımız configure ettiğimiz yapı aşağıdadır. Bu bağlantıyı kurmak için yukarıda import ettiğimiz 'create_engine' fonksiyonunu kullanacağız.
engine = create_engine(
    url=SQLALCEMY_DATABASE_URL,
    connect_args={
        'check_same_thread': False
    }
)

# Yukarıda import ettiğimiz sessionmaker() fonksiyonu ile veri tabanında bir oturum oluşturacağız CRUD operasyonlarında aktif olarka bu oturum üzerinden işlemleri yürüteceğiz.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# bind => yeni oluşturulan sesion nesnesi ile yukarıda yaratılan engine ile ilişkilendirilmeisni sağlar.
# autoflush => her yeni session nesnesi oluşturduğumuzda ayarları temizleme işlemi için kullanılır. biz aynı auth bilgileri ile devame deceğiz.
# autocommit => SQLALCEMY autocommit olmadan kullandığımızda session.commit() ve session.rollback() fonksiyonlarını çağırma işlemlerinin durumunu manuel olarak yönetmeyi sağlıyoruz.

# declarative_base() fonksiyonu kullanarak bir nesne yaratıyoruz. Yaratılan bu nesneyi model oluştururken ihtiyaç duyacağım özellikleri bana teslim etmesi için kullanacağım.
Base = declarative_base()
