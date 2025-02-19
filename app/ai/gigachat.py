import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import uuid
import json


CLIENT = st.secrets["CLIENT_ID"]
SECRET = st.secrets["CLIENT_SECRET"]

class GigaChatAPI:
    def __init__(self):
        self.client = CLIENT
        self.secret = SECRET
        self.url_oath = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        self.url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"


    def get_access_token(self) -> str:
        payload = {"scope": "GIGACHAT_API_PERS"}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid.uuid4())
        }
        result = requests.post(
            url=self.url_oath, 
            headers=headers, 
            auth=HTTPBasicAuth(CLIENT, SECRET), 
            data=payload,
            verify=False
        )

        access_token = result.json()["access_token"]

        return access_token

    def send_prompt(self, msg: str, access_token: str):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": msg}]
        }

        response = requests.post(
            url=self.url,
            headers=headers,
            json=payload,
            verify=False
        )

        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")

        try:
            return response.json()["choices"][0]["message"]["content"]
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON response: {response.text}") from e
        except KeyError as e:
            raise Exception(f"Unexpected response format: {response.json()}") from e

    def translate_prompt(self, prompt: str) -> str:
        access_token = self.get_access_token()
        prompt = f"Переведи на английский, не давай никаких пояснений: {prompt}"
        response = self.send_prompt(prompt, access_token)
        print(response)
        return response
