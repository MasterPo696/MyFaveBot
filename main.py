import streamlit as st
from app.utils.smart_logs import SmartLogs
from app.ai.tools import AITools
from app.auth.login import login_page
from database.database import get_db
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ai = AITools()

def main():
    st.title("My ChatBot")
    
    # Initialize request counter in session state
    if 'request_count' not in st.session_state:
        st.session_state.request_count = 0
    
    # Check if user is logged in
    if 'user' not in st.session_state:
        # Show chat interface for first 5 requests
        if st.session_state.request_count >= 5:
            st.warning("You've reached the limit of 5 requests. Please register to continue.")
            login_page()
            return
    
    ai.initialize_session_state()
    ai.display_chat_history()

    if user_prompt := st.chat_input("Message"):
        try:
            # Increment request counter ONLY for non-logged users
            if 'user' not in st.session_state:
                st.session_state.request_count += 1
            
            st.chat_message("user").write(user_prompt)
            st.session_state.message.append({"role": "user", "content": user_prompt})
            
            if "нарисуй" in user_prompt.lower() or "draw" in user_prompt.lower():
                ai.handle_image_generation(user_prompt)
            else:
                ai.handle_chat_response(user_prompt)
                
            # Show registration prompt ONLY for non-logged users when reaching limit
            if 'user' not in st.session_state and st.session_state.request_count >= 5:
                st.warning("You've reached the limit of 5 requests. Please register to continue.")
                login_page()
                
        except Exception as e:
            st.toast(str(e))

if __name__ == "__main__":
    main()