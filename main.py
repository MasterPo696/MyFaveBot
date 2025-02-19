import streamlit as st
from app.ai.gigachat_api import GigaChatAPI
from app.ai.starrai_api import StarRaiAPI

giga = GigaChatAPI()


st.title("My ChatBot")

if "access_token" not in st.session_state:
    try:
        st.session_state.access_token = giga.get_access_token()
        st.toast("Access token received")
    except Exception as e:
        st.toast(e)

if "message" not in st.session_state:
    try:
        st.session_state.message = [{"role": "ai", "content": "Hey, how can i help you today?"}]
    except Exception as e:
        st.toast(e)

for msg in st.session_state.message:
    try:
        st.chat_message(msg["role"]).write(msg['content'])
    except Exception as e:
        st.toast(e)

if user_prompt := st.chat_input("Message"):
    try:
        st.chat_message("user").write(user_prompt)
        st.session_state.message.append({"role": "user", "content": user_prompt})
        if user_prompt.startswith("нарисуй"):
            star = StarRaiAPI()
            with st.spinner("Generating image..."):
                try:
                    image_list = star.send_prompt(user_prompt)
                    if image_list and len(image_list) > 0:
                        # Создаем колонки для отображения изображений
                        cols = st.columns(2)
                        for idx, image_data in enumerate(image_list):
                            # Проверяем наличие URL и его корректность
                            if 'url' in image_data and image_data['url']:
                                col_idx = idx % 2
                                with cols[col_idx]:
                                    st.image(image_data['url'], caption=f"Image {idx+1}")
                        # Сохраняем ссылки на изображения в истории сообщений
                        image_urls = [img['url'] for img in image_list if 'url' in img and img['url']]
                        if image_urls:
                            st.session_state.message.append({"role": "ai", "content": f"Generated images: {image_urls}"})
                        else:
                            st.error("Не удалось получить URL изображений")
                    else:
                        st.error("Не удалось сгенерировать изображения")
                except Exception as img_error:
                    st.error(f"Ошибка при генерации изображения: {str(img_error)}")
        else:
            with st.spinner("Generating response..."):
                    response = giga.send_prompt(user_prompt, st.session_state.access_token)
                    # st.toast(response)
                    st.chat_message("ai").write(response)
                    st.session_state.message.append({"role": "ai", "content": response})
            
    except Exception as e:
        st.toast(e)
    
    