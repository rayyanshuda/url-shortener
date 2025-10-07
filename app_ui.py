import streamlit as st
import requests
import os

# Optional: use environment variable if available (for future flexibility)
BACKEND_URL = os.getenv("BACKEND_URL", "https://url-shortener-5wwm.onrender.com")

st.set_page_config(page_title="Rayyan's URL Shortener", page_icon="🔗", layout="centered")

st.title("🔗 Rayyan's URL Shortener")
st.caption("Powered by FastAPI + PostgreSQL + Redis")

url = st.text_input("Enter a long URL:")
if st.button("Shorten URL"):
    try:
        res = requests.post(f"{BACKEND_URL}/shorten", json={"long_url": url})
        if res.status_code == 200:
            short_url = res.json()["short_url"]
            st.success(f"Short URL: {short_url}")
            st.write(f"[Open Link]({short_url})")
        else:
            st.error(f"Error: {res.text}")
    except Exception as e:
        st.error(f"Backend not reachable: {e}")
