# মনের কথা — ৪ পেজ + Admin Website

## পেজ
1. `/` — আত্মনির্ভরতা ও অনুপ্রেরণার ছবি
2. `/consultants` — Consultant-এর উক্তি ও পরামর্শ
3. `/services` — সেবা, appointment flow, contact
4. `/info` — FAQ, status, privacy/terms তথ্য

## ব্যবহারকারীর ফর্ম
- `/book` — appointment
- `/anonymous` — anonymous post
- `/contact` — contact message
- `/status` — Reference ID দিয়ে status ও admin reply দেখা

## Admin
Login: `/admin/login`

Admin ID: `admin`
Admin Password: `MonerKotha@2026!`

Admin dashboard:
- appointment দেখা
- status (Pending/Confirmed/Cancelled) পরিবর্তন
- customer-এর জন্য reply লেখা
- anonymous/contact messages দেখা
- reply/status সংরক্ষণ

## Run locally
Windows:
1. Python 3.10+ install করুন।
2. Command Prompt খুলুন।
3. এই folder-এ গিয়ে: `pip install flask werkzeug`
4. তারপর: `python app.py`
5. Browser: `http://127.0.0.1:5000`

## Production
এই Flask app একটি Python-supported server-এ deploy করুন (যেমন Render, Railway, PythonAnywhere বা VPS)। SQLite starter হিসেবে আছে; production-এ PostgreSQL ব্যবহার করা ভালো।

## গুরুত্বপূর্ণ
- Admin password লাইভ করার আগে পরিবর্তন করুন।
- HTTPS ব্যবহার করুন।
- প্রকৃত consultant-এর verified qualification/registration যোগ করুন।
- Privacy, consent, refund, terms এবং data retention policy পেশাদারভাবে review করুন।
- Payment integration (Nagad/bKash) এখনো secure gateway হিসেবে wired নয়; user-এর সঙ্গে যোগাযোগ করে মূল্য জানানোর জন্য site-এ fixed price দেখানো হয়নি।
