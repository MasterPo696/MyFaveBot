import streamlit as st
import requests
import time

class StarRaiAPI:
    def __init__(self):
        self.base_url = "https://api.starryai.com"  # Исправленный URL
        self.api_key = st.secrets["STARRAI_API"]  # Проверить, что ключ загружается корректно

    def send_prompt(self, prompt: str):
        headers = {
            'X-API-Key': self.api_key,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        payload = {
            "model": "lyra",  # Указана модель
            "aspectRatio": "square",  # Соотношение сторон
            "highResolution": False,  # Отключено высокое разрешение
            "images": 4,  # Количество изображений
            "steps": 20,  # Количество шагов генерации
            "initialImageMode": "color",  # Режим начального изображения
            "prompt": prompt  # Сам запрос
        }

        response = requests.post(
            f"{self.base_url}/creations/",  # Правильный эндпоинт
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            creation_id = response.json().get('id')
            return self._wait_for_generation(creation_id, headers)
        else:
            raise Exception(f"Failed to create generation: {response.status_code} - {response.text}")

    def _wait_for_generation(self, creation_id: str, headers: dict):
        """Функция проверяет статус генерации изображения"""
        while True:
            response = requests.get(
                f"{self.base_url}/creations/{creation_id}/",
                headers=headers
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'completed':
                    return data['images']  # Возвращаем список с URL изображений
                elif data.get('status') == 'failed':
                    raise Exception("Image generation failed")
            
            time.sleep(5)  # Ждём 5 секунд перед повторной проверкой
            