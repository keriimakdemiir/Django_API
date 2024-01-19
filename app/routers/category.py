from fastapi import APIRouter, Depends, status, HTTPException, Path
from settings import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from models import Category

# API rouuter sınıfında instance alıyoruz. Uygulamaya gelen talepleri 'router' nesnesi ile dizayn ettiğimiz url'ler ile yönlendireceğiz.
router = APIRouter()


# database bağlantısını açıp işimiz bitince kapatıyoruz
def get_db_conn():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Yukarıda kullandığımız yield terimi ilgili objeyinin önceliğini belirtmek içindir yani yiled ifadesinden sonra gelen kodun response dönüldükten sonra execute edilir. Bunu yapmamızda ki sebep uygulamamızın daha hızlı çalışmasını temin etmek içindir. Çünkü veri tabanından bilgi alıp ön tarafa getirirken bize performans gerekmektedir. Asenkron programlama ile aynı mantığı burada düşünebiliriz. İşlem bittikten sonra execute end olduktan sonra bağlantı her zaman kapatılacaktır. Yatartılan "db" isimli nesneyi GC RAM'in Heap alanından uçuracaktır. Bu da her talep başına bir veri tabanı bağlantısı oluşturulacağı anlamına gelmektedir. Bunun tam tersi mantık ise singleton desing pattern ile üretilen database bağlantısı kuran nesnelerdir.


# DIP uymak için aşağıda ki kodu yazdık. DIP ile yakından ilintili olan IoC prensibine de muhakkak bakın.
db_dependency = Annotated[Session, Depends(get_db_conn)]


# DTO (Data Transfer Object), UI (UserInterface) yani arayüzden ki biz arayüz olarak SwagerIU kullanacağız API'yi test etmek için. Bu arayüzden kullanıcınun girdiği data'yı burada ki fonksiyonlarımıza taşıyacak olan aracı yapıdır. DTO'lar çift yönlü olarak çalıştırılabilinirler. Yani hem arayüzden gelen data'yı fonksiyona hemde fonksiyoun database'den çağıdığı datayı UI taşımak için kullanılamkatadır.
class CategoryDTO(BaseModel):
    name: str
    description: str = Field(min_length=2, max_length=100)


@router.post(path='/category/create', status_code=status.HTTP_201_CREATED)
async def create_category(db: db_dependency, category_dto: CategoryDTO):
    model = Category()

    # mapping işlemi yapıyoruz. yani UI'dan gelen category_dto ile taşınan data'nın alanları ile model nesnemizin alanlarını eşliyoruz.
    model.name = category_dto.name
    model.description = category_dto.description
    model.is_active = True

    db.add(model)
    db.commit()

    return {
        'status_code': 201,
        'transaction': 'Successful'
    }


@router.get(path='/', status_code=status.HTTP_200_OK)
async def get_all_categories(db: db_dependency):
    data = db.query(Category).all()

    if data is not None:
        return data

    raise HTTPException(
        status_code=404,
        detail='There is no data'
    )


@router.get('/category/{category_id}', status_code=status.HTTP_200_OK)
async def get_category_by_id(db: db_dependency, category_id: int = Path(gt=0)):
    data = db.query(Category).filter(Category.id == category_id).first()

    if data is not None:
        return data

    raise HTTPException(
        status_code=404,
        detail='Category not found'
    )


# put() vs patch()
@router.put('/category/{category_id}', status_code=status.HTTP_200_OK)
async def update_category(db: db_dependency, category_dto: CategoryDTO, category_id: int = Path(gt=0)):
    data = db.query(Category).filter(Category.id == category_id).first()

    if data is None:
        raise HTTPException(
            status_code=404,
            detail='Category not found'
        )

    data.name = category_dto.name
    data.description = category_dto.description

    db.add(data)
    db.commit()

    return {
        'status_code': 200,
        'transaction': 'Successful'
    }


@router.delete('/category/{category_id}', status_code=status.HTTP_200_OK)
async def delete_category(db: db_dependency, category_id: int = Path(gt=0)):
    data = db.query(Category).filter(Category.id == category_id).first()

    if data is None:
        raise HTTPException(
            status_code=404,
            detail='Category not found'
        )

    db.query(Category).filter(Category.id == category_id).delete()

    db.commit()

    return {
        'status_code': 200,
        'transaction': 'Successful'
    }