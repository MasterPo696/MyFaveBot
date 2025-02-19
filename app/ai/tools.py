import streamlit as st
from app.ai.gigachat import GigaChatAPI
from app.ai.starrai import StarRaiAPI

class AITools:
    def __init__(self):
        # Создаём экземпляр GigaChatAPI, который будет использоваться всеми методами
        self.giga = GigaChatAPI()

    def initialize_session_state(self):
        if "access_token" not in st.session_state:
            try:
                st.session_state.access_token = self.giga.get_access_token()
                st.toast("Access token received")
            except Exception as e:
                st.toast(e)

        if "message" not in st.session_state:
            try:
                st.session_state.message = [
                    {"role": "ai", "content": "Hey, how can I help you today?"}
                ]
            except Exception as e:
                st.toast(e)

    def display_chat_history(self):
        for msg in st.session_state.message:
            try:
                st.chat_message(msg["role"]).write(msg["content"])
            except Exception as e:
                st.toast(e)

    def handle_image_generation(self, prompt):
        star = StarRaiAPI()

        prompt = prompt.replace("нарисуй", "").replace("draw", "")

        with st.spinner("Generating image..."):
            try:
                try:
                    eng_prompt = self.giga.translate_prompt(prompt)
                except Exception as e:
                    eng_prompt = prompt
                
                image_list = star.send_prompt(eng_prompt)
                if image_list and len(image_list) > 0:
                    cols = st.columns(2)
                    for idx, image_data in enumerate(image_list):
                        if 'url' in image_data and image_data['url']:
                            col_idx = idx % 2
                            with cols[col_idx]:
                                st.image(image_data['url'], caption=f"Image {idx+1}")
                    
                    image_urls = [img['url'] for img in image_list if 'url' in img and img['url']]
                    if image_urls:
                        st.session_state.message.append({
                            "role": "ai",
                            "content": f"Generated images: {image_urls}"
                        })
                    else:
                        st.error("Не удалось получить URL изображений")
                else:
                    st.error("Не удалось сгенерировать изображения")
            except Exception as img_error:
                st.error(f"Ошибка при генерации изображения: {str(img_error)}")

    def handle_chat_response(self, prompt):
        with st.spinner("Generating response..."):
            try:
                response = self.giga.send_prompt(prompt, st.session_state.access_token)
                st.chat_message("ai").write(response)
                st.session_state.message.append({
                    "role": "ai",
                    "content": response
                })
            except Exception as e:
                st.toast(e)
