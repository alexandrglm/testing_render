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

# TESTING DIFFERENT SCHEMAS
projects = [
    {
        'order': '404',
        'type': 'project',
        'id': '404',
        'metadata': {
            'title': 'Not Every Mistake is Truly a Mistake ',
            'subtitle': '',
            'desc': 'Sometimes, mistakes are masterpieces, unlike this error 404 page. ',
            'snapshot': '', 
            'date': '2025-03-01',
            'author': 'admin',
            'category': '404, designs'
        },
        'size': 'wide',
        'hidden': True
    },
    {
        'order': '01',
        'type': 'project',
        'id': '01',
        'metadata': {
            'title': 'The Most Complex "Simple Hello World" site',
            'subtitle': 'Hello World Subtitle',
            'desc': 'No frills, no HTML fuss—just Python',
            'date': '2025-03-02',
            'author': 'admin',
            'category': 'tag1, tag2'
        },
        'size': 'default',
        'hidden': False
    },
    {
        'order': '02',
        'type': 'project',
        'id': '02',
        'metadata': {
            'title': 'CSS Advanced Hello World',
            'desc': 'A less simpler HelloWorld screen CSS made with parallax effect and floating bubbles, fully over-hardcoded for no reason.',
            'date': '2025-03-05',
        },
        'size': 'wide',
        'hidden': False
    },
    {
        'order': '03',
        'type': 'blog',
        'metadata': {
            'title': 'My first blog post here',
            'subtitle': 'Blog',
            'link': 'greetings',
            'desc': 'Description wrapper for blog post test lorem ipsum bla bla bla',
            'snapshot': 'greetings.png',
            'date': '2025-04-25',
            'author': 'Alexandr Gomez',
            'category': 'greetings, definitions'
        },
        'size': 'default',
        'hidden': False
    },
    {
        'order': '04',
        'type': 'project',
        'id': '03',
        'metadata': {
            'title': 'App Test 01, Logic performed via JS',
            'subtitle': '',
            'desc': 'App Test 01: AMSTRAD Color Tool converter using JavaScript.',
            'date': '2025-03-17',
            'author': '',
            'category': 'projects'
        },
        'size': 'default',
        'hidden': False
    },
    {
        'order': '05',
        'type': 'project',
        'id': '04',
        'metadata': {
            'title': 'App Test 02, but Logic performed at Back-End',
            'subtitle': '',
            'desc': 'App Test 02: AMSTRAD Color Tool converter using Python. Zero Front-end drama.',
            'date': '2025-04-01',
            'category': ''
        },
        'size': 'default',
        'hidden': False
    },
    {
        'order': '06',
        'type': 'project',
        'id': '05',
        'metadata': {
            'title': 'InspectorView Demo',
            'subtitle': '',
            'desc': 'App Test 01: AMSTRAD Color Tool converter using JavaScript.',
            'author': 'admin',
        },
        'size': 'default',
        'hidden': False
    },
    {
        'order': '07',
        'type': 'blog',
        'metadata': {
            'title': 'My 2nd blog post here',
            'subtitle': 'Blog',
            'link': 'more-greetings',
            'desc': 'Description wrapper for blog post test lorem ipsum bla bla bla',
            'snapshot': 'greetings.png',
            'date': '2025-05-25',
            'category': 'greetings, definitions'
        },
        'size': 'wide',
        'hidden': False
    }
]




# projects = [
#     {'id': '14', 'title': 'React Deploys (1): Bottega\'s VSCode Analytics', 'desc': 'Bottega\'s React 14 web app for student VSCode analytics, adapted to React 18+ and served via Flask.'},
#     {'id': '13', 'title': 'Studying Tools 2: Advanced Web Scraper       ', 'desc': 'URL-to-Markdown concept tool with custom CSS remapping (Custom DIVs, Bootstrap, components). MongoDB used as persistent storage.'},
#     {'id': '12', 'title': '(py)MongoDB Atlas WebShell                   ', 'desc': 'A MongoDb Atlas webshell for database manipulation using PyMongo (sync) and SocketIO in async mode.'},
#     {'id': '11', 'title': '3D / VR Showcase test                        ', 'desc': 'First approach to developing VR/Augmented Reality environments.'},
#     {'id': '10', 'title': 'WebShell                                     ', 'desc': 'Web-based interactive shell framework with real-time frontend-backend communication using Flask and Socket.IO'},
#     {'id': '09', 'title': 'Studying Tools 1: MarkDown Web Server        ', 'desc': 'Parsing Markdown into HTML. A basic framework with auto-generated indexes for a documentation showroom.'},
#     {'id': '08', 'title': 'Simple JSON DataBase Handler                 ', 'desc': 'An excuse to learn about dunders, @property decorators, Rest API GET/POST/PUT/PATCH/DETELE methods, and so on, and so forth.'},
#     {'id': '07', 'title': '(Where) Is-ISS?                              ', 'desc': 'Yet another ISS live tracking tool using "requests" and JSON, but simplest.'},
#     {'id': '06', 'title': 'Naiz Headlines, Now                          ', 'desc': 'Scraping headlines like if I were a junior devel. Best news and headlines scraping tool using Py. "requests" from naiz.eus.'},
#     {'id': '05', 'title': 'InspectorView Demo                           ', 'desc': 'Why is this div not centered? Simple concept for a web CSS inspector tool.'},
#     {'id': '04', 'title': 'App Test 02, but Logic performed at Back-End ', 'desc': 'App Test 02: AMSTRAD Color Tool converter using Python. Zero Front-end drama.'},
#     {'id': '03', 'title': 'App Test 01, Logic performed via JS          ', 'desc': 'App Test 01: AMSTRAD Color Tool converter using JavaScript.'},
#     {'id': '02', 'title': 'CSS Advanced Hello World                     ', 'desc': 'A less simpler HelloWorld screen CSS made with parallax effect and floating bubbles, fully over-hardcoded for no reason.'},
#     {'id': '01', 'title': 'The Most Complex "Simple Hello World" site   ', 'desc': 'No frills, no HTML fuss—just Python.'},
#     {'id': '404', 'title': 'Not Every Mistake is Truly a Mistake        ', 'desc': 'Sometimes, mistakes are masterpieces, unlike this error 404 page. '}
# ]

static_pages = [
    {'pathName' : 'about', 'link' : 'about/about.html'},
    {'pathName' : 'contact', 'link' : 'contact/contact.html'},
    {'pathName' : 'admin', 'link' : 'admin/panel.html'}
]

allowed_root_files = [
    {'filename' : 'robots.txt'},
    {'filename' : 'version.txt'}
]

