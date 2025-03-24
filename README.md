# Web Services Test & Showroom

## Updated to 2025, March.

****

Welcome to **Web Services Test**, a repository designed for experimenting with web services using a Python backend, along with various frontend implementations.

****

## 📌 Project Structure

```
/testing_render
├── back.py            # Main backend server
├── requirements.txt   # Python dependencies
├── static/            # Static assets for each project
│   ├── 01/
│   ├── ...
│   ├── 404/
├── templates/         # HTML web renders for each project
│   ├── 01/
│   ├── ...
│   ├── 404/
│   ├── main.html
├── data/              # Project-specific data storage
│   ├── 01/
│   ├── ...
│   ├── 404/
├── projectXX.py       # Project XX backend logic
```

- **Backend**: Python
- **Frontend**: HTML, CSS, JavaScript

## ⚙️ How to Run

These web services are available online: [JustLearn.ing](https://justlearn.ing/)

To run them locally:

1. Install dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

2. Start the backend at `localhost:8080`:
   
   ```bash
   python back.py
   ```

---

## 📂 Projects

A collection of experimental web services and tools:

| ID  | Title                                      | Description                                                                                                  |
| --- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| 01  | **The Most Complex "Simple Hello World"**  | No frills, no HTML fuss—just Python.                                                                         |
| 02  | **CSS Advanced Hello World**               | A Hello World with parallax effects and floating bubbles—over-engineered on purpose.                         |
| 03  | **Back-End Only as Server**                | App Test 01: AMSTRAD Color Tool converter using JavaScript.                                                  |
| 04  | **Back-End as Logic**                      | App Test 02: AMSTRAD Color Tool converter using Python. Zero Front-end drama.                                |
| 05  | **InspectorView Demo**                     | Why is this `div` not centered? A simple concept for a CSS inspector tool.                                   |
| 06  | **Naiz Headlines, Now**                    | Scraping headlines like a junior dev. A Python `requests` scraper for naiz.eus.                              |
| 07  | **(Where) Is-ISS?**                        | Yet another ISS live tracking tool using `requests` and JSON—the simplest one yet.                           |
| 08  | **Profile Info Getter/Setter**             | Learning `__init__`, `__main__`, and `@property` decorators by serving a "Profiles/Records" framework.       |
| 09  | **Study Framework 1: Markdown Web Server** | Parses Markdown into HTML with auto-generated indexes for a documentation showroom.                          |
| 10  | **WebSockets Shell**                       | A web-shell initial project using WebSockets. No __eval()__ used. Real and open.                             |
| 11  | **3D / VR Showcase test**                  | First approach to developing VR/Augmented Reality environments. Library used: A-FRAME /  THREE.js                          |        
| 12  | **(py)MongoDB Atlas WebShell**             | A MongoDb Atlas webshell for database manipulation using PyMongo (sync) and SocketIO in async mode.                          |                         
| 404 | **Not Every Mistake is Truly a Mistake**   | Sometimes, mistakes are masterpieces... but not this error 404 page.                          |




