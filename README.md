# 🎬 MovieWeb App

A Flask web application that allows users to register, log in, and manage their favorite movies with reviews.

## Features

- User Registration and Authentication
- Add, Edit, and Delete Movies
- Add, Edit, View, and Delete Reviews
- User-specific movie lists (only accessible by the owner)
- Simple and clean Bootstrap-styled UI

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** Jinja2, Bootstrap 5
- **Data Layer:** Custom DataManager (in-memory or file-based or database)
- **Session Management:** Flask built-in session


## 📁 Project Structure

```bash
moviweb_app/
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── users.html
│   ├── user_movies.html
│   ├── ...
├── static/
│   ├── css/
│   └── images/
├── auth_routes.py
├── user_routes.py
├── movie_routes.py
├── review_routes.py
├── main_routes.py
├── auth_utils.py
├── data_manager.py
├── app.py
├── config.py
└── README.md