# 📝 Django Blog Application

A full-featured Blog Application built using Django and Django REST Framework.
Demonstrates real-world backend and frontend integration with authentication, authorization, filtering, pagination, and a clean UI.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-5.2+-green)
![DRF](https://img.shields.io/badge/DRF-3.14+-red)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **JWT Authentication** | Access & Refresh tokens with auto-refresh |
| **Blog Posts** | Create, edit, publish posts with Draft/Published status |
| **Authorization** | Only authors can edit their posts; drafts are private |
| **Filters & Search** | Filter by status, search by keywords, tag-based filtering |
| **Pagination** | Paginated listing with filter preservation |
| **Comments** | Users can add comments to posts |
| **Share Post** | Share posts via email |
| **Responsive UI** | Card-based layout with Font Awesome icons |

---

## 🛠️ Tech Stack

**Backend:**
- Python, Django, Django REST Framework, SimpleJWT

**Frontend:**
- Django Templates, HTML, CSS, JavaScript, Font Awesome

**Database:**
- SQLite / PostgreSQL

---

## 📁 Project Structure

    blog/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── api_views.py
    │
    ├── templates/
    │   └── blog/
    │       └── post/
    │           ├── list.html
    │           ├── detail.html
    │           ├── add_blog.html
    │           ├── edit_blog.html
    │           ├── search.html
    │           └── share.html
    │
    └── static/
        ├── css/
        │   └── blog.css
        └── js/
            └── authFetch.js

---

## 🚀 Setup Instructions

**1. Clone repository**

    git clone https://github.com/nitustar/MyProjects.git
    cd mysite

**2. Create virtual environment**

    python -m venv venv
    source venv/bin/activate

On Windows:

    venv\Scripts\activate

**3. Install dependencies**

    pip install -r requirements.txt

**4. Apply migrations**

    python manage.py migrate

**5. Create superuser**

    python manage.py createsuperuser

**6. Run server**

    python manage.py runserver

Open `http://127.0.0.1:8000/` in your browser.

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/token/` | POST | Get access & refresh token |
| `/api/token/refresh/` | POST | Refresh access token |
| `/blog/api/posts/add/` | POST | Add new post |
| `/blog/api/posts/<id>/edit/` | PUT | Edit post |

---

## 👤 Author

**Nitesh Kumar** - Python Developer | Django | REST APIs

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/nitesh-kumar-software-dev)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/nitustar)

---
