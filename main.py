from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ==========================================
# 1. NÓ DE PERSISTÊNCIA (Banco de Dados)
# ==========================================
# Se a variável de ambiente DATABASE_URL existir (no Render), usa ela. Se não, cria um arquivo SQLite local.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./estoque.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ItemDB(Base):
    __tablename__ = "itens"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    quantidade = Column(Integer)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)


# ==========================================
# 2. NÓ DE APLICAÇÃO (API REST)
# ==========================================
app = FastAPI(title="Sistema de Estoque Distribuído")

class ItemCreate(BaseModel):
    nome: str
    quantidade: int

@app.post("/itens/", summary="Adicionar um novo item no banco de dados")
def criar_item(item: ItemCreate):
    db = SessionLocal()
    novo_item = ItemDB(nome=item.nome, quantidade=item.quantidade)
    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)
    db.close()
    return novo_item

@app.get("/itens/", summary="Listar todos os itens do banco de dados")
def listar_itens():
    db = SessionLocal()
    itens = db.query(ItemDB).all()
    db.close()
    return itens