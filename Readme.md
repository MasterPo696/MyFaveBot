# 🤖 AI Chat & Image Generation App

A Streamlit application that provides chat functionality using GigaChat API and image generation with StarrAI. Features Google OAuth authentication and SQLite database for user management.

## ✨ Features

- 💬 Chat interface powered by GigaChat API
- 🎨 Image generation capabilities via StarrAI
- 🔐 User authentication with Google OAuth 
- 💾 Local SQLite database for user data
- 🔄 5 free requests for non-authenticated users
- 📱 Clean and responsive UI
- 🌐 Support for Russian and English prompts

## 🚀 Installation

1. Clone the repository
```bash
git clone https://github.com/MasterPo696/MyFaveBot
cd MyFaveBot
```


2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up configuration
```bash
cp .streamlit/secrets.example.toml .streamlit/secrets.tom
```

Then edit `.streamlit/secrets.toml` with your actual API keys and credentials.

## 🔑 Configuration

You need to obtain the following API keys:
- GigaChat API credentials (CLIENT_ID and CLIENT_SECRET)
- StarrAI API key

Add these to your `.streamlit/secrets.toml` file.

## 🏃‍♂️ Running the App

```bash
streamlit run main.py
```


## 💡 Usage

- Start chatting normally for text conversations
- Type "нарисуй" or "draw" followed by your description to generate images
- The app will automatically detect whether to use chat or image generation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/yourusername/your-repo-name/issues).

Important steps after setting up these files:
If you haven't already committed your secrets, remove them from Git tracking:

```bash
git rm --cached .streamlit/secrets.toml
git commit -m "Remove secrets from git tracking"
```
