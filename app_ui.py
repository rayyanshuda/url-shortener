import streamlit as st
import requests
import os

st.set_page_config(page_title="Rayyan's URL Shortener", page_icon="🔗", layout="centered")

st.title("🔗 Rayyan's URL Shortener")
st.caption("Add a custom alias (optional) to personalize your link!")

url = st.text_input("Enter a long URL:")
alias = st.text_input("Custom alias (optional):")

if st.button("Shorten URL"):
    if not url:
        st.warning("Please enter a URL.")
    else:
        with st.spinner("Generating short link..."):
            try:
                BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
                res = requests.post(f"{BACKEND_URL}/shorten", json={"long_url": url, "custom_alias": alias or None})
                if res.status_code == 200:
                    data = res.json()
                    short_url = data["short_url"]
                    st.success(f"Short URL: {short_url}")
                    st.markdown(f"[Open Link]({short_url})")
                elif res.status_code == 400:
                    error_detail = res.json().get("detail", "Bad Request.")
                    st.warning(f"{error_detail}")
                else:
                    # catch validation or duplicate alias errors
                    st.error(f"Error {res.status_code}: {res.json().get('detail', res.text)}")
            except Exception as e:
                st.error(f"Backend not reachable: {e}")
