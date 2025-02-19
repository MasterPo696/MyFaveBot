import streamlit as st
from app.auth.total_auth import AuthService
from database.database import get_db
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def callback_page():
    if 'flow' not in st.session_state:
        st.error("Authentication flow not found")
        return

    try:
        flow = st.session_state['flow']
        code = st.experimental_get_query_params().get("code", [None])[0]
        
        if code:
            flow.fetch_token(code=code)
            credentials = flow.credentials
            
            db = next(get_db())
            auth_service = AuthService(db)
            user_info = auth_service.verify_google_token(credentials.id_token)
            
            if user_info:
                st.session_state['user'] = user_info
                st.success("Successfully logged in with Google!")
                st.experimental_rerun()
            else:
                st.error("Failed to verify Google token")
    except Exception as e:
        st.error(f"Authentication failed: {str(e)}")

if __name__ == "__main__":
    callback_page()