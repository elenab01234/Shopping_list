import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer,Float, Boolean


WORK_DIR = Path(__file__).parent.parent
load_dotenv(WORK_DIR / ".env")

USERNAME = os.getenv("MYSQL_USERNAME")
PASSWORD = os.getenv("MYSQL_PASSWORD")
mysql_db_url = f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost:3306/shoppinglistdata'

engine = create_engine(mysql_db_url)

Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()

class ShoppingListItem(Base):
    __tablename__ = 'shoppinglistitemtable'
    index = Column(Integer, primary_key=True, autoincrement=True)
    Item = Column(String(50), nullable=False)
    Price = Column(Float(precision=53))
    Quantity = Column(Integer)
    Bought = Column(Boolean)
    Category = Column(String(50), nullable=False)

    def to_dict(self):
        return {"index": self.index,
                "Item": self.Item,
                "Price": self.Price,
                "Quantity": self.Quantity,
                "Bought": self.Bought,
                "Remove": False,
                "Category": self.Category
                }

class ShoppingListCategory(Base):
    __tablename__ = 'shoppinglistcategories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Category = Column(String(50), nullable=False)


Base.metadata.create_all(engine)
session.commit()
