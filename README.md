# Web Services Test & Showroom

Welcome to this repository, designed to be deployed on my server as a showcase for web services, utilizing a Python-Flask backend, with a frontend built using Flask-Jinja, also React for some projects.

This project is hosted on Render.com **using a free-tier account**, which may result in longer loading times due to the limitations of the free plan.

To address these and other limitations, some projects are specifically designed to bypass most of these constraints, including:

- Web-based Server Terminal
- Cron Jobs to maintain server always up
- Free Persistent Storage storing files into MongoDB
- SocketIO Multi-threading tasks
- Pre-loaded Dependencies for a faster compilation time

Apart from fully-developed projects, various sketches, ideas, and proof-of-concept applications can be found, built using technologies I'm currently studying, as this repo serves as my personal toybox.

Feel free to explore, experiment, and contribute to the evolution of this web services playground!

---
***
## 📂 Projects

A collection of experimental web services and tools:

| ID  | Title                                      | Description                                                                                                                      |
| --- | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| 01  | **The Most Complex "Simple Hello World"**  | No frills, no HTML fuss—just Python.                                                                                             |
| 02  | **CSS Advanced Hello World**               | A Hello World with parallax effects and floating bubbles—over-engineered on purpose.                                             |
| 03  | **Back-End Only as Server**                | App Test 01: AMSTRAD Color Tool converter using JavaScript.                                                                      |
| 04  | **Back-End as Logic**                      | App Test 02: AMSTRAD Color Tool converter using Python. Zero Front-end drama.                                                    |
| 05  | **InspectorView Demo**                     | Why is this `div` not centered? A simple concept for a CSS inspector tool.                                                       |
| 06  | **Naiz Headlines, Now**                    | Scraping headlines like a junior dev. A Python `requests` scraper for naiz.eus.                                                  |
| 07  | **(Where) Is-ISS?**                        | Yet another ISS live tracking tool using `requests` and JSON—the simplest one yet.                                               |
| 08  | **Profile Info Getter/Setter**             | Learning `__init__`, `__main__`, and `@property` decorators by serving a "Profiles/Records" framework.                           |
| 09  | **Studying Tools 1: Markdown Web Server**  | Parses Markdown into HTML with auto-generated indexes for a documentation showroom.                                              |
| 10  | **WebSockets Shell**                       | A web-shell initial project using WebSockets. No __eval()__ used. Real and open.                                                 |
| 11  | **3D / VR Showcase test**                  | First approach to developing VR/Augmented Reality environments. Library used: A-FRAME /  THREE.js                                |
| 12  | **(py)MongoDB Atlas WebShell**             | A MongoDb Atlas webshell for database manipulation using PyMongo (sync) and SocketIO in async mode.                              |
| 13  | **Studying Tools 2: Advanced Web Scraper** | URL-to-Markdown concept tool with custom CSS remapping (Custom DIVs, Bootstrap, components). MongoDB used as persistent storage. |
| 14  | **React Deploys (1): Bottega's VSCode Analytics** | Bottega\'s React 14 web app for student VSCode analytics, adapted to React 18+ and served via Flask. |
| 404 | **Not Every Mistake is Truly a Mistake**   | Sometimes, mistakes are masterpieces... but not this error 404 page.                                                             |

---

## 📌 Project Structure

- **Backend**: Python, Flask.
- **Frontend**: HTML, CSS, JavaScript. React (TSX/SaSS compilers)
```
/testing_render
├── back.py            # Main backend server
|
├── requirements.txt   # Python dependencies
|
├── build.sh           # React deployment script
|
├── data/              # Project-specific data storage (React deploys, files outside from /static/, ...)
│   ├── 01/
│   ├── ...
│   └── 404/
|
├── node_modules       # NPM requirements included for a faster server up
|
├── server/            # Server modules
│   ├── mail.py
│   └── ...
|
├── static/            # Static assets for each project
│   ├── 01/
│   ├── ...
│   └── 404/
|
├── templates/         # HTML web renders for each project
│   ├── 01/
│   ├── ...
│   ├── 404/
│   └── main.html
|
└── projectXX.py       # Project XX backend logic, as blueprints.
```
---

## ⚙️ How to Run

These web services are available online: [JustLearn.ing](https://justlearn.ing/)

To run them locally:

1. Install dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

2. Server is fully self-deployed (including React compilation, needed bash scripts and others) by starting the main `back.py`:
   
   ```bash
   python back.py
   ```

3. Configue the secrets like this:


### .env file
```
Server things:

SERVER_CORS -> Big string, comma-separated, with allowed CORS domain:ports

SERVER_EX_IP -> Excluded IP list, non-quotted, comma-separated, for exclusions in logs
SERVER_EX_HOST -> Excluded HOST (non-quotted, comma-separated). Full and Partial host domain capable.

SMTP_ACCOUNT -> Mail used for Contact Form daemon
SMTP_PASSWORD
SMTP_PORT
SMTP_SERVER
SMTP_USER


MONGO_SERVER_DB -> Logs are backuped using Atlas-MongoDB specific collection and DB
MONGO_SERVER_COLLECTION 


MongoDB Atlas things (Server logs, project13, persistant storage, ...):

Mind about how MongoDB URIs are used in many scripts:

MONGO_URI = f'mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST_1}:{MONGO_PORT},{MONGO_HOST_2}:{MONGO_PORT},{MONGO_HOST_3}:{MONGO_PORT}/?replicaSet={MONGO_SETS}&authSource=admin'


MONGO_HOST_1 -> Your own Cluster on Atlas-MongoDB Host-00-00
MONGO_HOST_2 -> Your own Cluster on Atlas-MongoDB Host-00-01
MONGO_HOST_3 -> Your own Cluster on Atlas-MongoDB Host-00-02
MONGO_PORT
MONGO_SETS
MONGO_USER
MONGO_PASS

Project 10: Web Shell
shell_uri -> Must contain domain or ip:port, otherwise WebShell wont enable prompt

Project 13: Scrappy
PROJECT13_DB -> MongoDB database name for DB in use.
PROJECT13_FILTERS -> MongoDB collection name for scrap filters.
PROJECT13_PAGES -> MongoDB collection name for a persistant storage of scraped pages.


Project 14:
API_BOTTEGA= Bottega Student API for VSCode Analytics App (you may use the public API 211e3ba5-273a-489c-a376-691c68db7527 )
```

---

