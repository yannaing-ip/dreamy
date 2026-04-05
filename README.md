# Dreamy — Dream-Based Social Network API

A RESTful social networking backend where users connect through shared dreams. Users subscribe to dream categories, post feed entries tagged with those dreams, and follow each other to build a personalized social experience.

Built with **Django 6** and **Django REST Framework**, authenticated via **JWT**.

---

## Features

- **JWT Authentication** — register, login, and refresh tokens
- **Custom User Model** — email-based login with first/last name and username
- **Dream Subscriptions** — users subscribe to dream categories that define their interests
- **Feed System** — create posts tagged with dreams, with public/private/protected visibility
- **Follow System** — follow/unfollow users; follower and following counts maintained automatically
- **Like & Comment** — toggle likes and comment on feeds; counts updated via Django signals
- **Visibility Control** — feeds can be public, private (followers only), or protected
- **User Search** — search users by username, first name, or last name
- **Profile View** — view any user's profile with their feeds (respects visibility rules)
- **CI/CD** — GitHub Actions workflow for automated testing

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| Framework | Django 6.0.3 |
| API | Django REST Framework 3.17 |
| Auth | SimpleJWT |
| Database | SQLite (dev) / PostgreSQL (prod) |
| CI | GitHub Actions |

---

## Project Structure

```
dreamy/
├── core/               # Project config (settings, urls, wsgi)
├── accounts/           # User model, auth, follow system
├── feeds/              # Feed posts, likes, comments
├── dreams/             # Dream categories
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/yannaing-ip/dreamy.git
cd dreamy

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env  # then edit .env with your values

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

---

## Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## API Reference

Base URL: `/api/`

### Auth

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/register/` | Register a new user | No |
| POST | `/api/login/` | Login and get tokens | No |
| POST | `/api/token/refresh/` | Refresh access token | No |
| GET | `/api/me/` | Get current user profile | Yes |

#### Register
```json
POST /api/register/
{
  "email": "user@example.com",
  "username": "yannaing",
  "first_name": "Yan",
  "last_name": "Naing",
  "password": "securepassword"
}
```

#### Login
```json
POST /api/login/
{
  "email": "user@example.com",
  "password": "securepassword"
}
```
Response:
```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```

---

### Users & Follow

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/search/?q=<query>` | Search users | Yes |
| GET | `/api/profile/<id>/` | View user profile | Yes |
| POST | `/api/users/<id>/follow/` | Follow or unfollow a user | Yes |
| GET | `/api/users/<id>/followers/` | List followers | Yes |
| GET | `/api/users/<id>/following/` | List following | Yes |

---

### Dreams

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/dream/` | List all dreams (supports `?search=`) | Yes |
| POST | `/api/dream/` | Subscribe to a dream | Yes |
| POST | `/api/dreams/<id>/remove/` | Unsubscribe from a dream | Yes |

#### Subscribe to a Dream
```json
POST /api/dream/
{
  "dream_id": 1
}
```

---

### Feeds

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/feeds/` | List feeds (visibility-aware) | Yes |
| POST | `/api/feeds/` | Create a new feed post | Yes |
| GET | `/api/feeds/<id>` | Get a specific feed | Yes |
| DELETE | `/api/feeds/<id>/delete/` | Delete a feed (author only) | Yes |
| GET | `/api/feeds/<id>/likes/` | List users who liked | Yes |
| POST | `/api/feeds/<id>/likes/` | Toggle like | Yes |
| GET | `/api/feeds/<id>/comments/` | List comments | Yes |
| POST | `/api/feeds/<id>/comments/` | Add a comment | Yes |
| DELETE | `/api/feeds/<id>/comments/<comment_id>/delete/` | Delete a comment | Yes |

#### Create a Feed Post
```json
POST /api/feeds/
{
  "content": "I dreamed I was flying over mountains...",
  "visibility": "PL",
  "dreams": [1, 2]
}
```

Visibility options:
- `PL` — Public (visible to everyone)
- `PR` — Private (visible to followers only)
- `PT` — Protected

---

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <access_token>
```

Access tokens expire in **60 minutes**. Use `/api/token/refresh/` with your refresh token to get a new one.

---

## Running Tests

```bash
python manage.py test
```

CI runs automatically on every push to `main` via GitHub Actions.

---

## Author

**Yan Naing**
GitHub: [@yannaing-ip](https://github.com/yannaing-ip)

