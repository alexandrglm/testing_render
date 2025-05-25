# FILE:        ./server/mainObjects.py
# BRANCH:        server-stable


"""
Main Idea -> MongoDB (B)JSON Schema

-> If then SQL is used, empty fields should be present ( 'x key' : '')
-> Now, rendering order is elegible by using 'order' key-value
-> 'id' key remains for projects flask internal paths
-> Some key-values are MANDATORY, some others may be omitted

-> Static Pages still follow its own ruleset.

TEMPLATES

FOR PROJECTS:

{
    'order': 'MANDATORY (STRINGED INTEGER)',
    'type': 'project',
    'id': MANDATORY (STRINGED INTEGER)',
    'metadata': {
        'title': 'MANDATORY',
        'subtitle': 'OPTIONAL',
        'desc': 'OPTIONAL',
        'date': 'OPTIONAL',
        'author': 'OPTIONAL',
        'category': 'OPTIONAL tag1, tag2, tag3, ...'
    },
    'size': 'MANDATORY -> default, wide, mini, ... pending CSS designs',
    'hidden': BOOL MANDATORY
},

    
FOR BLOGS:

{
    'order': 'MANDATORY (STRINGED INTEGER)',
    'type': 'blog',
    'metadata': {
        'title': 'MANDATORY',
        'subtitle': 'OPTIONAL',
        'link': 'MANDATORY',
        'desc': 'OPTIONAL',
        'snapshot': 'MANDATORY <filename.png>',
        'date': 'AAAA-MM-DD MANDATORY',
        'author': 'OPTIONAL',
        'category': 'OPTIONAL tag1, tag2, tag3, ...'
    },
    'size': 'MANDATORY -> default, wide, mini, ... pending CSS designs',
    'hidden': BOOL MANDATORY
},

"""

projects = [
    {
    "order": "14",
    "type": "project",
    "id": "14",
    "metadata": {
        "title": "React Deploys (1): Bottega's VSCode Analytics",
        "subtitle": "My Fists React deploy",
        "desc": "Bottega's React 14 web app for student VSCode analytics, adapted to React 18+ and served via Flask.",
        "date": "2025-04-18",
        "author": "",
        "category": "react, metrics, TSX, SCSS"
    },
    "size": "wide",
    "hidden": False
    },
    {
    "order": "13",
    "type": "project",
    "id": "13",
    "metadata": {
        "title": "Advanced Web Scraper",
        "subtitle": "Student tools",
        "desc": "URL-to-Markdown concept tool with custom CSS remapping (Custom DIVs, Bootstrap, components). MongoDB used as persistent storage.",
        "date": "2025-05-12",
        "author": "",
        "category": "webscraping, markdown, mongodb"
    },
    "size": "default",
    "hidden": False
    },
    {
    "order": "12",
    "type": "project",
    "id": "12",
    "metadata": {
        "title": "(py)MongoDB Atlas WebShell",
        "subtitle": "PROJECT",
        "desc": "A MongoDb Atlas webshell for database manipulation using PyMongo (sync) and SocketIO in async mode.",
        "date": "2025-03-22",
        "author": "",
        "category": "mongodb, pymongo, webshell"
    },
    "size": "default",
    "hidden": False
    },
    {
    "order": "11",
    "type": "project",
    "id": "11",
    "metadata": {
        "title": "3D / VR Showcase test",
        "subtitle": "PROJECT",
        "desc": "First approach to developing VR/Augmented Reality environments.",
        "date": "2025-04-05",
        "author": "",
        "category": "vr, 3d, augmented-reality, openVR, openXR, THREE.js"
    },
    "size": "default",
    "hidden": False
    },
    {
    "order": "10",
    "type": "project",
    "id": "10",
    "metadata": {
        "title": "WebShell",
        "subtitle": "PROJECT",
        "desc": "Web-based interactive shell framework with real-time frontend-backend communication using Flask and Socket.IO",
        "date": "2025-05-20",
        "author": "",
        "category": "webshell, flask, socketio"
    },
    "size": "default",
    "hidden": False
    },
    {
    "order": "09",
    "type": "project",
    "id": "09",
    "metadata": {
        "title": "MarkDown Web Server",
        "subtitle": "Student Tools",
        "desc": "Parsing Markdown into HTML. A basic framework with auto-generated indexes for a documentation showroom.",
        "date": "2025-03-15",
        "author": "",
        "category": "markdown, webserver, documentation"
    },
    "size": "default",
    "hidden": False
    },
    {
    "order": "08",
    "type": "project",
    "id": "08",
    "metadata": {
        "title": "Simple JSON DataBase Handler",
        "subtitle": "PROJECT",
        "desc": "An excuse to learn about dunders, @property decorators, Rest API GET/POST/PUT/PATCH/DETELE methods, and so on, and so forth.",
        "date": "2025-04-30",
        "author": "",
        "category": "json, restapi, python, json, NoSQL"
    },
    "size": "default",
    "hidden": False
    },
    {
    "order": "07",
    "type": "project",
    "id": "07",
    "metadata": {
        "title": "(Where) Is-ISS?",
        "subtitle": "PROJECT",
        "desc": "Yet another ISS live tracking tool using \"requests\" and JSON, but simplest.",
        "date": "2025-05-08",
        "author": "",
        "category": "API Rest, tracking, ISS"
    },
    "size": "default",
    "hidden": False
    },
    {
    "order": "06",
    "type": "project",
    "id": "06",
    "metadata": {
        "title": "Naiz Headlines, Now",
        "subtitle": "PROJECT",
        "desc": "Scraping headlines like if I were a junior devel. Best news and headlines scraping tool using Py. \"requests\" from naiz.eus.",
        "date": "2025-03-28",
        "author": "",
        "category": "scraping, news, headlines"
    },
    "size": "default",
    "hidden": False
    },
    {
    "order": "05",
    "type": "project",
    "id": "05",
    "metadata": {
        "title": "InspectorView Demo",
        "subtitle": "PROJECT",
        "desc": "Why is this div not centered? Simple concept for a web CSS inspector tool.",
        "date": "2025-04-12",
        "author": "",
        "category": "css, inspector, debug, devtools"
    },
    "size": "default",
    "hidden": False
    },
    {
    "order": "04",
    "type": "project",
    "id": "04",
    "metadata": {
        "title": "App Test 02, but Logic performed at Back-End",
        "subtitle": "App Testing ",
        "desc": "AMSTRAD Colour Tool converter,but using Python. Zero Front-end drama.",
        "date": "2025-05-15",
        "author": "",
        "category": "backend, python, color-converter"
    },
    "size": "default",
    "hidden": False
    },
    {
    "order": "03",
    "type": "project",
    "id": "03",
    "metadata": {
        "title": "App Test 01, Logic performed via JS",
        "subtitle": "App Testing",
        "desc": "AMSTRAD Colour Tool converter, JS logic.",
        "date": "2025-03-10",
        "author": "",
        "category": "javascript, frontend, color-converter"
    },
    "size": "default",
    "hidden": False
    },
    {
    "order": "02",
    "type": "project",
    "id": "02",
    "metadata": {
        "title": "CSS Advanced Hello World",
        "subtitle": "PROJECT",
        "desc": "A less simpler HelloWorld screen CSS made with parallax effect and floating bubbles, fully over-hardcoded for no reason.",
        "date": "2025-04-25",
        "author": "",
        "category": "CSS, helloworld, frontend, CSS animation"
    },
    "size": "default",
    "hidden": False
    },
    {
    "order": "01",
    "type": "project",
    "id": "01",
    "metadata": {
        "title": "The Most Complex \"Simple Hello World\" site",
        "subtitle": "Hello World!",
        "desc": "No frills, no HTML fuss—just Python.",
        "date": "2025-05-05",
        "author": "",
        "category": "python, backend, Flask, helloworld"
    },
    "size": "default",
    "hidden": False
    },
    {
    "order": "404",
    "type": "project",
    "id": "404",
    "metadata": {
        "title": "Not Every Mistake is Truly a Mistake",
        "subtitle": "PROJECT",
        "desc": "Sometimes, mistakes are masterpieces, unlike this error 404 page.",
        "date": "2025-03-20",
        "author": "",
        "category": "error, 404, page"
    },
    "size": "default",
    "hidden": True
    }
]


static_pages = [
    {'pathName' : 'about', 'link' : 'about/about.html'},
    {'pathName' : 'contact', 'link' : 'contact/contact.html'},
    {'pathName' : 'admin', 'link' : 'admin/panel.html'}
]

allowed_root_files = [
    {'filename' : 'robots.txt'},
    {'filename' : 'version.txt'}
]
