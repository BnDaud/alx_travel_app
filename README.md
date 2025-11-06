# 🏡 Airbnb Clone Backend (Django)

This project is a backend implementation of a simplified **Airbnb-like platform**, built with **Django**.  
It provides APIs and data models to manage **users, property listings, bookings, and reviews**.

---

## 🚀 Features

- **Custom User Model** (`AbstractUser`)

  - Roles: `host`, `guest`, `admin`
  - UUID as primary key
  - Support for phone numbers

- **Property Listings**

  - Hosts can create, update, and delete listings
  - Each property has a UUID primary key, description, location, and nightly price

- **Bookings**

  - Guests can request bookings for properties
  - Tracks start/end dates, total price, and booking status (`Pending`, `Confirmed`, `Canceled`)

- **Reviews**

  - Guests can leave ratings (1–5 stars) and comments on listings
  - Ratings validated with both built-in and custom validators

- **Timestamps**
  - Automatic `created_at` and `updated_at` fields across models

---

## 🛠️ Tech Stack

- **Backend Framework**: Django (Python)
- **Database**: PostgreSQL / SQLite (development)
- **Auth**: Django’s built-in authentication system with custom user model
- **UUIDs**: Used for all primary keys

---

## 📂 Project Structure

---

## ⚙️ Models Overview

### 👤 User

- Custom user model with `UUID` as primary key
- Fields: `username`, `email`, `phone_number`, `role`, `created_at`

### 🏘️ Listing

- Belongs to a `host` (User)
- Fields: `name`, `description`, `location`, `price_per_night`, `created_at`, `updated_at`

### 📅 Booking

- Belongs to a `guest` (User) and a `listing`
- Fields: `start_date`, `end_date`, `total_price`, `status`

### ⭐ Review

- Belongs to a `listing`
- Fields: `rating` (1–5), `comment`, `created_at`, `updated_at`

---

## ▶️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/vectoredmatrix/alx_travel_app_0x00.git
cd alx_travel_app_0x00

python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser
# Terminal 1 — RabbitMQ broker
sudo service rabbitmq-server start
# or
rabbitmq-server
# Terminal 2 — Celery worker
celery -A alx_travel_app worker -l info


python manage.py runserver
```
