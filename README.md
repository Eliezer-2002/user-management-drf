# 🚀 User Management System – Django REST Framework

```bash
https://user-management-drf.onrender.com/
```

A **role-based User Management System** built using **Django REST Framework (DRF)** that provides secure authentication, authorization, pagination, and search features following REST best practices.

This project was developed **practically without relying on tutorials**, focusing on real-world backend development concepts.

---

## 🛠️ Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Authentication:** JWT (JSON Web Tokens)
- **Database:** SQLite (development)
- **API Features:** Pagination, Search, Permissions
- **Frontend:** HTML + css + JavaScript (Fetch API)

---

## ✨ Features

- 🔐 JWT-based authentication (Login & Protected APIs)
- 👤 User listing with pagination
- 🔍 Search users by username or email
- 🧑‍⚖️ Role-based access control (Admin / Authenticated users)
- 🛡️ Custom permissions using `BasePermission`
- ✏️ Create and update users via REST APIs
- 📄 Clean API responses with pagination metadata
- 📐 REST-compliant API design

---

## 📂 Project Structure

```bash
project/
│── accounts/
│ ├── views.py
│ ├── serializers.py
│ ├── permissions.py
│ ├── pagination.py
│ ├── page_urls.py
│ └── urls.py
│── static/
│ └── responsive.css
│── templates/
│ ├── layouts/
│ │ └── navbar.html
│ ├── base.html
│ ├── users.html
│── project/
│ └── settings.py
└── manage.py
```

---

## 🔑 Authentication
This project uses **JWT authentication**.

### Login
POST /api/token/

**Response:**
```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}

```

**Use the access token in headers:**

**Authorization:** Bearer < token >

| Method | Endpoint                  | Description     | Permission |
| ------ | ------------------------- | --------------- | ---------- |
| POST   | `/api/token/`             | Login           | Public     |
| GET    | `/api/users/`             | List users      | Admin only |
| POST   | `/api/users/create/`      | Create user     | Admin only |
| PATCH  | `/api/users/<id>/update/` | Update user     | Admin      |
| GET    | `/api/users/?search=`     | Search users    | Admin      |
| GET    | `/api/users/?page=`       | Paginated users | Admin      |


## 📄 Pagination & Search

Pagination implemented using PageNumberPagination

Search enabled via SearchFilter

**Example:**
/api/users/?page=2&search=john

---

## 🧠 Key Learnings

Proper use of DRF Generic Views

Difference between CreateAPIView and UpdateAPIView

Writing business logic inside serializers

Implementing custom permissions

Handling pagination & search on frontend

Secure API design using JWT

---

## 🧪 How to Run Locally

### Clone the repository

git clone https://github.com/your-username/your-repo.git
cd your-repo


### Create virtual environment

python -m venv env
source env/bin/activate


### Install dependencies

```bash
pip install -r requirements.txt
```

### Run migrations

```bash
python manage.py migrate
```

### Start server

```bash
python manage.py runserver
```

---

## 🎯 Future Improvements

Role-based permissions for multiple user types

API documentation using Swagger

Frontend using React

Deployment with PostgreSQL

---

## 👨‍💻 Author

Eliezer S

Aspiring Python Backend / Full Stack Developer

B.Sc Computer Science (2024)

---

## ⭐ Why This Project?

* This project demonstrates:

* Real backend problem solving

* Clean DRF architecture

* RESTful API design

* Practical development without tutorial dependency