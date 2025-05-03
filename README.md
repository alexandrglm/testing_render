# Web Services Test & Showroom

Welcome to this repository, designed to be deployed on my server as a showcase for web services, utilizing a Python-Flask backend, with a frontend built using HTML, CSS, and React (featuring real-time TSX/Sass compilation).

This project is hosted on Render.com **using a free-tier account**, which may result in longer loading times due to the limitations of the free plan.

To address these and other limitations, some projects are specifically designed to bypass most of these constraints, including:

- Web-based Server Terminal
- Cron Jobs with React Deployments
- Free Persistent Storage storing files into MongoDB
- SocketIO Multi-threading
- Pre-loaded Dependencies

Apart from fully-developed projects, various sketches, ideas, and proof-of-concept applications can be found, built using technologies I'm currently studying, as this repo serves as my personal toybox.

Feel free to explore, experiment, and contribute to the evolution of this web services playground!

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
__* You may need to configure an .env file including every needed secret settings in order to get a fully working projects.__
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
- **Frontend**: HTML, CSS, JavaScript. React (TSX/SCSS compilers)
```
/testing_render
├── back.py            # Main backend server
├── requirements.txt   # Python dependencies
├── build.sh           # React deployment script
├── static/            # Static assets for each project
│   ├── 01/
│   ├── ...
│   ├── 404/
├── templates/         # HTML web renders for each project
│   ├── 01/
│   ├── ...
│   ├── 404/
│   ├── main.html
├── data/              # Project-specific data storage (React deploys)
│   ├── 01/
│   ├── ...
│   ├── 404/
├── projectXX.py       # Project XX backend logic, as blueprints.
```

