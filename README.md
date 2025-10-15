# URL Shortener 
A full-stack URL shortening service built with FastAPI, PostgreSQL, Redis, and Streamlit.
The app lets users input a long URL (and optionally a custom alias) to generate a short, shareable link
that redirects seamlessly to the original destination.
<br>

Deployed using **Render** (backend & database) and **Streamlit Cloud** (frontend)


# Live Demo
Frontend (Streamlit): [Click Here](https://url-cut.streamlit.app/). <br>
Backend (FastAPI): [Click Here](https://url-shortener-5wwm.onrender.com/).

# Overview 
This project demonstrates end-to-end system design, covering:

- Backend API development with FastAPI
  
- Relational data modeling with SQLAlchemy + PostgreSQL

- Optional caching layer with Redis

- Frontend integration with Streamlit

- Cloud deployment and configuration management with environment variables

Users can:

- Shorten any valid URL.

- Add a custom alias (e.g. `/jordan-mid-se)`.

- Retrieve shortened URLs via API or UI.

- Be redirected instantly through the short link.

# Tech Stack

**Frontend**
- Streamlit - UI Framework for data apps
- REST API integration with `requests`

**Backend**
- FastAPI - High-performance web framework
- SQLAlchemy - ORM for database modeling
- PostgreSQL - main data store
- Redis - Caching and fast lookups
- Docker - Containerization for local development

**Deployment**
- Render - Backend + Postgres hosting
- Streamlit Cloud - Frontend deployment



## Local Development Setup

1. **Clone the repo**  

   ```bash
   git clone https://github.com/<your-username>/url-shortener.git
   cd url-shortener

2. **Create and activate a virtual environment**  

   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # windows

3. **Install Dependencies**  

   ```bash
   pip install -r requirements.txt

4. **Run PostgreSQL and Redis using Docker Compose**  

   ```bash
   docker-compose up -d
   # Run `docker ps` and you should see 3 container IDs

5. **Start the FastAPI backend**  

   ```bash
   uvicorn app.main:app --reload

6. **Start the Streamlit frontend**

   ```bash
   streamlit run app_ui.py


## Notes
- Your backend runs at `http://127.0.0.1:8000`
- Your Streamlit app runs at `http://localhost:8501`
- To stop Docker containers:
    ```bash
    docker-compose down
- Make sure your `.env` file is configured for local use.


### Author: Rayyan Huda

[rayyanhuda.com](https://rayyanhuda.com/)  

[LinkedIn](https://www.linkedin.com/in/rayyanhuda/)
