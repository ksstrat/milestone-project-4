# DEPLOYMENT

---

## Table of Contents
- [What you must customize](#what-you-must-customize)
- [Option A — Run locally (quick start)](#option-a--run-locally-quick-start)
- [Option B — Deploy to Heroku](#option-b--deploy-to-heroku)
- [Post deployment admin setup](#postdeployment-admin-setup)
- [Optional: Google OAuth](#optional-google-oauth)

---

**This guide is intended to help you clone the project as easily as possible and get it up and running quickly.**

---

## What you must customize

- **SECRET_KEY** — Generate your own (never reuse someone else’s).
- **YOUR_APP_NAME** — Your unique Heroku app name (e.g., `my-pixelpulse-demo`).
- **ALLOWED_HOSTS / CSRF_TRUSTED_ORIGINS** — Match your domain(s) or Heroku URL.
- **CLOUDINARY_URL** (optional) — Needed for image uploads if using Cloudinary.
- **Google OAuth creds** (optional) — Only if you want Google sign‑in.

---

## Option A — Run locally (quick start)

1) **Clone & install**
```bash
git clone https://github.com/ksstrat/milestone-project-4.git
cd milestone-project-4
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2) **Environment**

Create `.env` with at least:
```
DEBUG=True
SECRET_KEY=YOUR_RANDOM_SECRET
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000
SITE_ID=1
# Optional if you want uploads locally via Cloudinary
# CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

3) **Migrate & run**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1

---

## Option B — Deploy to Heroku

1) **Create app & DB**
```bash
heroku create YOUR_APP_NAME
heroku addons:create heroku-postgresql:essential
```

2) **Config vars**
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=YOUR_RANDOM_SECRET
heroku config:set ALLOWED_HOSTS=YOUR_APP_NAME.herokuapp.com
heroku config:set CSRF_TRUSTED_ORIGINS=https://YOUR_APP_NAME.herokuapp.com
heroku config:set SITE_ID=1
# Optional media:
# heroku config:set CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

3) **Procfile (project root)**
```procfile
release: python manage.py migrate
web: gunicorn milestone_project_4.wsgi --log-file -
```

4) **Deploy**
```bash
# first deploy (often easiest to disable collectstatic initially)
heroku config:set DISABLE_COLLECTSTATIC=1
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku config:unset DISABLE_COLLECTSTATIC
```
Please rebuild after that.

Ensure `WhiteNoiseMiddleware` is in settings and `STATIC_ROOT` is set (see project README/DEPLOYMENT).

---

## Post deployment admin setup

1) **Sites**
- Admin → **Sites** → set domain to `YOUR_APP_NAME.herokuapp.com` (or your custom domain).

2) **Moderation & Users**
- Create test users, assign permissions via Admin if needed.

---

## Optional: Google OAuth

If you don’t need social login, you can skip this entire section.

If you want Google sign‑in:
- **Google Console redirect URI:**  
  `https://YOUR_APP_NAME.herokuapp.com/accounts/google/login/callback/`  
  (locally: `http://localhost:8000/accounts/google/login/callback/`)
- Admin → **Social accounts → Social applications → Add (Google)** and attach your Site.
- Set `GOOGLE_CLIENT_ID` / `GOOGLE_SECRET` in your .env

---
