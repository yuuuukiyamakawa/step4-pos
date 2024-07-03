# ORM（SQLalchemy）によるデータ規則と構成

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import ForeignKey, String, CHAR, VARCHAR, Integer, DATETIME


class Base(DeclarativeBase):
    pass

class Product_master(Base):
    __tablename__ = 'product_master'
    PRD_ID:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    CODE:Mapped[str] = mapped_column(CHAR(13))
    NAME:Mapped[str] = mapped_column(VARCHAR(50))
    PRICE:Mapped[int] = mapped_column()

class Transaction(Base):
    __tablename__ = 'transaction'
    TRD_ID:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    DATETIME:Mapped[str] = mapped_column()
    EMP_CD:Mapped[int] = mapped_column()
    STORE_CD:Mapped[int] = mapped_column()
    POS_NO:Mapped[int] = mapped_column()
    TOTAL_AMT:Mapped[int] = mapped_column()

class Transaction_detail(Base):
    __tablename__ = 'transaction_detail'
    DTL_ID:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    TRD_ID:Mapped[int] = mapped_column(ForeignKey("transaction.TRD_ID"))
    PRD_ID:Mapped[int] = mapped_column(ForeignKey("product_master.PRD_ID"))
    PRD_CODE:Mapped[str] = mapped_column(CHAR(13))
    PRD_NAME:Mapped[str] = mapped_column(VARCHAR(50))
    PRD_PRICE:Mapped[int] = mapped_column()