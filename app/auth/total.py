import streamlit as st
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.orm import Session
from app.models.user import User
import bcrypt

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.google_client_id = st.secrets["GOOGLE_CLIENT_ID"]
    
    def verify_google_token(self, token):
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), self.google_client_id)
            return idinfo
        except ValueError:
            return None
    
    def login_user(self, email: str, password: str):
        user = self.db.query(User).filter(User.email == email).first()
        if user and user.check_password(password):
            return user
        return None
        
    
    def register_user(self, email: str, password: str, name: str):
        # Проверка на существование пользователя
        if self.db.query(User).filter(User.email == email).first():
            return None
            
        # Создание нового пользователя
        user = User(
            email=email,
            name=name
        )
        user.set_password(password)
        
        try:
            self.db.add(user)
            self.db.commit()
            return user
        except Exception:
            self.db.rollback()
            return None