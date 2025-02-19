import streamlit as st
from app.auth.total import AuthService
from database.database import get_db
from app.auth.google import create_google_oauth_flow

def login_page():
    st.title("Login")
    
    login_type = st.radio("Login method:", ["Email/Password", "Google"])
    
    if login_type == "Email/Password":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            db = next(get_db())
            auth_service = AuthService(db)
            user = auth_service.login_user(email, password)
            
            if user:
                st.session_state['user'] = user
                st.success("Successfully logged in!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")
    
    else:
        if st.button("Login with Google"):
            flow = create_google_oauth_flow()
            auth_url, _ = flow.authorization_url(prompt='consent')
            st.session_state['flow'] = flow
            st.markdown(f'<meta http-equiv="refresh" content="0;url={auth_url}">', unsafe_allow_html=True)