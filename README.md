# 🔗 ShortLink. - Modern Full-Stack URL Shortener

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlalchemy.org/)
[![uv](https://img.shields.io/badge/Package_Manager-uv-DE5D43?style=for-the-badge)](https://github.com/astral-sh/uv)

A fast, lightweight, and modern full-stack URL shortener application built with **FastAPI**, **SQLAlchemy**, **SQLite**, and a responsive frontend dashboard.

---

## ✨ Features

- ✂️ **Instant URL Shortening**: Convert long web links into unique 6-character random codes.
- 🔀 **Smart Redirection**: Redirect shortened links seamlessly to their target destinations (automatically handles missing `http://` or `https://` prefixes).
- 📊 **Click Analytics**: Tracks total click counts for every shortened URL.
- 🕒 **Timestamp Logs**: Records creation (`createdAt`) and last update (`updatedAt`) timestamps.
- 🔄 **Link Management**: Regenerate short codes or delete existing links easily.
- 🎨 **Responsive Frontend**: Includes an intuitive web interface for managing your shortened links.
- ⚡ **CORS Support**: Ready for frontend integration across different domains or local ports.

---

## 🛠️ Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM & Database**: [SQLAlchemy](https://www.sqlalchemy.org/) with [SQLite](https://www.sqlite.org/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Package Manager**: [`uv`](https://github.com/astral-sh/uv)

### Frontend
- **Structure**: HTML5
- **Styling**: CSS3 (Responsive Design)
- **Scripting**: Vanilla JavaScript (Fetch API)

---

## 📂 Project Structure

```text
url-shortener/
├── app/
│   └── app.py          # FastAPI application, models, routes & database configuration
├── frontend/
│   ├── index.html      # Web dashboard UI
│   ├── script.js       # Frontend API integration logic
│   └── style.css       # Custom styles
├── main.py             # Server entry point
├── pyproject.toml      # Project dependencies and configuration
├── uv.lock             # Lockfile for reproducible environment
└── README.md           # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** (Python 3.14+ recommended)
- **uv** (Fast Python package installer and resolver)

If you don't have `uv` installed, install it via:
```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/me7di-code/url-shortener.git
   cd url-shortener
   ```

2. **Install Dependencies**
   Using `uv`:
   ```bash
   uv sync
   ```
   *(Or using traditional `pip`: `pip install -r requirements.txt` if exported)*

---

## 🏃 Running the Application

### 1. Start the Backend Server

Run the development server using `uv`:
```bash
uv run main.py
```

Alternatively, launch with `uvicorn` live reload:
```bash
uv run uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

The API server will run at `http://localhost:8000`.

### 2. Access the Interactive API Docs

Once the backend is running, explore and test the endpoints directly in your browser:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 3. Open the Frontend Dashboard

Simply open `frontend/index.html` in your favorite web browser or serve it using any HTTP server (e.g. VS Code Live Server).

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description | Request Body / Params |
| :--- | :--- | :--- | :--- |
| `POST` | `/shorten` | Shorten a new URL | `{"url": "https://example.com"}` |
| `GET` | `/{code}` | Redirect to destination URL & increment click count | `code` (path parameter) |
| `GET` | `/all` | Retrieve all shortened URLs | None |
| `POST` | `/update/{code}` | Regenerate short code for a URL | `code` (path parameter) |
| `DELETE` | `/delete/{code}` | Delete a shortened link | `code` (path parameter) |

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
Project inspired by https://roadmap.sh/projects/url-shortening-service
