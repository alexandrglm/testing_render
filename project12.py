############################################################################
# Project 12: (Py)MongoDB Atlas WebShell
#
#
################
from flask import Blueprint, render_template
from flask_socketio import emit
from pymongo import MongoClient
import json
from bson import json_util
import os
from dotenv import load_dotenv

############################################################################
# Blueprint project12
################################
project12 = Blueprint('project12', __name__)

@project12.route('/')
def render_project12():
    return render_template('12/index_12.html')

############################################################################
# Secrets now using .env
################################
load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS')
MONGO_HOST_1 = os.getenv('MONGO_HOST_1')
MONGO_HOST_2 = os.getenv('MONGO_HOST_2')
MONGO_HOST_3 = os.getenv('MONGO_HOST_3')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_SETS = os.getenv('MONGO_SETS')

############################################################################
# Mongodb uri constgruction
################################
MONGO_URI = f'mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST_1}:{MONGO_PORT},{MONGO_HOST_2}:{MONGO_PORT},{MONGO_HOST_3}:{MONGO_PORT}/?replicaSet={MONGO_SETS}'

############################################################################
# Classes para el menu, y los comandos habituales
################################
class Menus:

    def __init__(self):
        self.current_menu = "main_menu"
        self.client = None
        self.db_in_use = None
        self.collection_in_use = None

    def get_menu(self):

        if self.current_menu == "main_menu":
            return self.get_main_menu()
        
        elif self.current_menu == "connection_menu":
            return self.get_connection_menu()
        
        elif self.current_menu == "database_menu":
            return self.get_database_menu()
        
        elif self.current_menu == "collection_menu":
            return self.get_collection_menu()
        
        else:
            return "DEBUG: Menu error, check class menu"

    def get_main_menu(self):
        
        return """
<strong>--- (Py)MongoDB Atlas Start menu ---</strong><br>
1. Login to MongoDB
2. Exit
"""

    def get_connection_menu(self):
        return """
<strong>--- Connection Operations ---</strong><br>
1. Connect using .env URI
2. Enter MongoDB URI manually
3. Back to main menu
"""

    def get_database_menu(self):
        db_name = self.db_in_use.name if self.db_in_use is not None else "None"
        return f"""
<strong>--- Database Operations ---</strong><br>
<strong>Database in use: {db_name}</strong><br>
1. List databases
2. Select a database
3. Create a new database
4. Delete a database
5. Back to connection menu
"""

    def get_collection_menu(self):
        db_name = self.db_in_use.name if self.db_in_use is not None else "None"
        collection_name = self.collection_in_use.name if self.collection_in_use is not None else "None"
        return f"""
<strong>--- Collection & Document Operations ---</strong><br>
<strong>Database in use: {db_name}</strong>
<strong>Collection in use: {collection_name}</strong><br>
1. List Collections
2. Select a Collection
3. Create a Collection
4. Remove a Collection
----
5. Find ALL Documents
6. Find one/many Documents
----
7. Insert One document
8. Insert Many Documents
----
9. Update a document
----
10. Delete a document
----
11. Back to database menu
"""

class MenuComunes:

    def __init__(self, menu_manager, client):

        self.menu_manager = menu_manager
        self.client = client

    def comunes(self, command):

        if command == 'menu':

            return {
                'output': self.menu_manager.get_main_menu(),
                'raw_output': ''
            }
        
        elif command == 'clear':

            return {
                'output': '\n' * 100,
                'raw_output': ''
            }
        
        elif command == 'help':
            return {
        'output': '''
<strong>(Py)MongoDB Shell v.0.1 - Help</strong>

<strong>Available Commands:</strong>
1. <strong>menu</strong>: Show the current menu options.
2. <strong>clear</strong>: Clear the terminal screen.
3. <strong>help</strong>: Display this help message.
4. <strong>exit</strong>: Disconnect from MongoDB and exit the application.

<strong>Workflow:</strong>
To interact with MongoDB, follow these steps:
1. <strong>Connect to MongoDB</strong>:
    - Use the connection menu to connect to a MongoDB server.
    - You can either use the default connection or provide a custom URI.
2. <strong>Select a Database</strong>:
    - Once connected, select a database from the list or create a new one.
3. <strong>Select a Collection</strong>:
    - After selecting a database, choose a collection to work with.
    - You can list existing collections or create a new one.
4. <strong>Perform Operations</strong>:
    - Once a collection is selected, you can perform CRUD operations:
        - <strong>Insert</strong>: Add new documents to the collection.
        - <strong>Find</strong>: Query documents in the collection.
        - <strong>Update</strong>: Modify existing documents.
        - <strong>Delete</strong>: Remove documents from the collection.

<strong>Common Operations:</strong>
- To list all databases, use the database menu.
- To list all collections in a database, use the collection menu.
- To insert a document, provide a JSON object.
- To query documents, provide a JSON filter.


<strong>Example of use:</strong>
1. Connect to MongoDB using the connection menu.
2. Select a database (e.g., "test").
3. Select a collection (e.g., "Books").
4. Insert a document: {"name": "John", "age": 30}.
5. Query documents: {"age": {"$gt": 25}}.
6. Update a document: {"name": "John"}, {"$set": {"age": 31}}.
7. Delete a document: {"name": "John"}.

<strong>Note:</strong>
- Use JSON format for queries, inserts, updates, and deletes. Don't worry about multi-lines and indentation.
- 
        ''',
        'raw_output': ''
    }
        
        elif command == 'exit':

            if self.client:

                self.client.close()
                
                self.client = None

            return {
                'output': '\n<h2>Thanks for testing this project. Bye!</h2>',
                'raw_output': '\nAtlas Server disconnected!\n'
            }
        
        else:

            return None

menu_manager = Menus()
menu_comunes = MenuComunes(menu_manager, menu_manager.client)





############################################################################
# Main: Lot of fixes pending
################################
# Raw server responses (unformatted, for server output)
def capturing_Atlas(response):

    if isinstance(response, (list, dict)):
        
        return '\nAtlas Server response: \n' + json_util.dumps(response, indent=4)
    
    return '\nAtlas Server response: \n' + str(response)
############################################################################
# JSON input queries' parser,
################################
# Rude and pending to fix
def process_json_input(json_lines):
    
    try:
        
        json_data = ''.join(json_lines)

        json_as_dict = json.loads(json_data)
        
        return json_as_dict
    
    except json.JSONDecodeError as e:

        raise ValueError(f'DEBUG: JSON construction failed -> {str(e)}')
################################
# Notice: 
# Socketio using gevent NEEDS a different invoking method
# The first webshell (project10) does not works with gevent (no async).
# In order to allow both blueprints compatibility, this is the way to get working async's socketios
# 
# Pending a lot of fixes (Delete sequential logic, data inputs, ...)
################################
def socketio_opers(socketio):
    ################################
    # socketio endpoint
    @socketio.on('connect')
    def connections_managment():

        menu_manager.current_menu = "main_menu"
        
        emit('execute_command_response', {'output': menu_manager.get_main_menu()})

    @socketio.on('execute_command')
    def socketio_commander(data):
        
        command = data.get('command', '').strip()

        if not command:
        
            emit('execute_command_response', {
                'output': '\n<h3>Error: No command provided.</h3>',
                'raw_output': ''
            })
        
            return

        try:
            
            if menu_manager.current_menu == "main_menu":
                
                if command == '1':
                
                    menu_manager.current_menu = "connection_menu"
        
                    emit('execute_command_response', {
                        'output': menu_manager.get_connection_menu(),
                        'raw_output': ''
                    })
                
                elif command == '2':
        
                
                    emit('execute_command_response', {
                        'output': '\n<h2>Thanks for testing this project. Bye!</h2>',
                        'raw_output': ''
                    })
                
                
                elif command in ['menu', 'clear', 'help', 'exit']:
    
                    response = menu_comunes.comunes(command)
                   
                
                    if response:
                
                        emit('execute_command_response', response)
                                
                else:
                
                    emit('execute_command_response', {
                        'output': '\n<h3>Input error. Please Type "menu" to see options, "clear" to clear the screen, and "exit" to exit.</h3>',
                        'raw_output': ''
                    })

            
            elif menu_manager.current_menu == "connection_menu":
                
                if command == '1':
                
                    try:
                
                        menu_manager.client = MongoClient(MONGO_URI)
                
                        response = menu_manager.client.admin.command('ping')
                
                        menu_manager.current_menu = "database_menu"
                
                        emit('execute_command_response', {
                            'output': '\n<h2>Connected to MongoDB.</h2>\n' + menu_manager.get_database_menu(),
                            'raw_output': capturing_Atlas(response)
                        })
                    
                    except Exception as e:
                
                        emit('execute_command_response', {
                            'output': f'\n<h3>Error connecting to MongoDB: {str(e)}</h3>',
                            'raw_output': capturing_Atlas(str(e))
                        })
                
                elif command == '2':
                
                    emit('execute_command_response', {
                        'output': '\n<h2>Please enter entire URI starting with "mongodb://"</h2>',
                        'raw_output': ''
                    })
                
                    menu_manager.current_menu = "awaiting_uri"
                
                elif command == '3':
                
                    menu_manager.current_menu = "main_menu"
                
                    emit('execute_command_response', {
                        'output': menu_manager.get_main_menu(),
                        'raw_output': ''
                    })
                
                elif command in ['menu', 'clear', 'help', 'exit']:
    
                    response = menu_comunes.comunes(command)
                   
                
                    if response:
                        emit('execute_command_response', response)
                
                
                else:
                
                    emit('execute_command_response', {
                        'output': '\n<h3>Input error. Please Type "menu" to see options, "clear" to clear the screen, and "exit" to exit.</h3>',
                        'raw_output': ''
                    })

            elif menu_manager.current_menu == "awaiting_uri":
                
                
                uri = command
                
                
                try:
                
                    menu_manager.client = MongoClient(uri)
                
                    response = menu_manager.client.admin.command('ping')
                

                    menu_manager.current_menu = "database_menu"
                
                    emit('execute_command_response', {
                        'output': '\n<h2>Connected to MongoDB.</h2>\n' + menu_manager.get_database_menu(),
                        'raw_output': capturing_Atlas(response)
                    })
                
                
                except Exception as e:
                
                    emit('execute_command_response', {
                        'output': f'\n<h3>Error connecting to MongoDB: {str(e)}</h3>',
                        'raw_output': capturing_Atlas(str(e))
                    })

            
            elif menu_manager.current_menu == "database_menu":
                
                if command == '1':
                

                    try:
                
                        databases = menu_manager.client.list_database_names()
                
                        emit('execute_command_response', {
                            'output': f'\n<strong>Databases: <h3>{", ".join(databases)}</h3></strong>\n' + menu_manager.get_database_menu(),
                            'raw_output': capturing_Atlas(databases)
                        })
                    
                    except Exception as e:
                

                        emit('execute_command_response', {
                            'output': f'\n<h3>Error listing databases: {str(e)}</h3>',
                            'raw_output': capturing_Atlas(str(e))
                        })
                
                
                elif command == '2':
                
                    emit('execute_command_response', {
                        'output': '\n<h2>Please enter the database name:</h2>',
                        'raw_output': ''
                    })
                
                    menu_manager.current_menu = "awaiting_db_name"
                
                
                elif command == '3':
                
                    emit('execute_command_response', {
                        'output': '\n<h2>Please enter the new database name:</h2>',
                        'raw_output': ''
                    })
                
                    menu_manager.current_menu = "awaiting_new_db_name"
                
                elif command == '4':
                
                    emit('execute_command_response', {
                        'output': '\n<h2>Please enter the database name to delete:</h2>',
                        'raw_output': ''
                    })
                
                    menu_manager.current_menu = "awaiting_db_to_delete"
                
                elif command == '5':
                
                    menu_manager.current_menu = "connection_menu"
                
                    emit('execute_command_response', {
                        'output': menu_manager.get_connection_menu(),
                        'raw_output': ''
                    })
                
                elif command in ['menu', 'clear', 'help', 'exit']:
    
                    response = menu_comunes.comunes(command)
                   
                    if response:
                
                        emit('execute_command_response', response)
                
                else:
                
                    emit('execute_command_response', {
                        'output': '\n<h3>Input error. Please Type "menu" to see options, "clear" to clear the screen, and "exit" to exit.</h3>',
                        'raw_output': ''
                    })

            elif menu_manager.current_menu == "awaiting_db_name":
                
                db_name = command.strip()
                
                if db_name:
                
                    try:
                
                        databases = menu_manager.client.list_database_names()
                
                        if db_name in databases:
                
                            menu_manager.db_in_use = menu_manager.client[db_name]
                
                            menu_manager.current_menu = "collection_menu"
                
                            emit('execute_command_response', {
                                'output': f'\n<h2>Using database: {db_name}</h2>\n' + menu_manager.get_collection_menu(),
                                'raw_output': capturing_Atlas(db_name)
                            })
                        
                
                        else:
                
                            emit('execute_command_response', {
                                'output': f'\n<h3>Error: Database "{db_name}" does not exist.</h3>\n' + menu_manager.get_database_menu(),
                                'raw_output': capturing_Atlas(f'Database "{db_name}" does not exist.')
                            })
                
                            menu_manager.current_menu = "database_menu"
                    
                    except Exception as e:
                
                        emit('execute_command_response', {
                            'output': f'\n<h3>Error selecting database: {str(e)}</h3>',
                            'raw_output': capturing_Atlas(str(e))
                        })
                
                        menu_manager.current_menu = "database_menu"
                
                else:
                
                    emit('execute_command_response', {
                        'output': '\n<h3>Error: No DB name provided.</h3>\n' + menu_manager.get_database_menu(),
                        'raw_output': capturing_Atlas('No DB name provided.')
                    })
                
                    menu_manager.current_menu = "database_menu"

            elif menu_manager.current_menu == "awaiting_new_db_name":
                
                
                db_name = command.strip()
                
                
                if db_name:
                
                    try:
                
                        menu_manager.db_in_use = menu_manager.client[db_name]
                

                        menu_manager.current_menu = "collection_menu"
                
                        emit('execute_command_response', {
                            'output': f'\n<h2>Database \'{db_name}\' has been created.</h2>\n' + menu_manager.get_collection_menu(),
                            'raw_output': capturing_Atlas(db_name)
                        })
                    
                
                    except Exception as e:
                
                        emit('execute_command_response', {
                            'output': f'\n<h3>Error creating database: {str(e)}</h3>',
                            'raw_output': capturing_Atlas(str(e))
                        })
                
                        menu_manager.current_menu = "database_menu"
                
                
                else:
                
                    emit('execute_command_response', {
                        'output': '\n<h3>Error: No DB name provided.</h3>\n' + menu_manager.get_database_menu(),
                        'raw_output': capturing_Atlas('No DB name provided.')
                    })
                
                    menu_manager.current_menu = "database_menu"

            
            elif menu_manager.current_menu == "awaiting_db_to_delete":
                
                db_name = command.strip()
                
                if db_name:
                    
                    confirm = data.get('confirm', '').strip()
                    
                    if confirm == 'YES':
                    
                        try:
                    
                            menu_manager.client.drop_database(db_name)
                    
                            emit('execute_command_response', {
                                'output': f'\n<h2>Database \'{db_name}\' deleted.</h2>\n' + menu_manager.get_database_menu(),
                                'raw_output': capturing_Atlas(f'Database "{db_name}" deleted.')
                            })
                    
                        except Exception as e:
                    
                            emit('execute_command_response', {
                                'output': f'\n<h3>Error deleting database: {str(e)}</h3>',
                                'raw_output': capturing_Atlas(str(e))
                            })
                    
                    else:
                    
                        emit('execute_command_response', {
                            'output': '\n<h2>Deletion canceled.</h2>\n' + menu_manager.get_database_menu(),
                            'raw_output': capturing_Atlas('Deletion canceled.')
                        })
                    
                    menu_manager.current_menu = "database_menu"
                
                else:
                    
                    emit('execute_command_response', {
                        'output': '\n<h3>Error: Database name not provided.</h3>\n' + menu_manager.get_database_menu(),
                        'raw_output': capturing_Atlas('Database name not provided.')
                    })
                    
                    menu_manager.current_menu = "database_menu"

            
            elif menu_manager.current_menu == "collection_menu":
            
                if command == '1':
                    
                    if menu_manager.db_in_use is not None:
                    
                    
                        try:
                    
                            collections = menu_manager.db_in_use.list_collection_names()
                    

                            emit('execute_command_response', {
                                'output': f'\n<strong>Collections: <h3>{", ".join(collections)}</h3></strong>\n' + menu_manager.get_collection_menu(),
                                'raw_output': capturing_Atlas(collections)
                            })
                        
                        except Exception as e:
                    
                            emit('execute_command_response', {
                                'output': f'\n<h3>Error listing collections: {str(e)}</h3>',
                                'raw_output': capturing_Atlas(str(e))
                            })
                    
                    else:
                    
                        emit('execute_command_response', {
                            'output': '\n<h3>Error: No database selected.</h3>\n' + menu_manager.get_collection_menu(),
                            'raw_output': capturing_Atlas('No database selected.')
                        })
                
            
                elif command == '2':
                    
                    emit('execute_command_response', {
                        'output': '\n<h2>Please enter the collection name:</h2>',
                        'raw_output': ''
                    })
                    
                    menu_manager.current_menu = "awaiting_collection_name"
                
            
                elif command == '3':
                    
                    emit('execute_command_response', {
                        'output': '\n<h2>Please enter the new collection name:</h2>',
                        'raw_output': ''
                    })
                    
                    menu_manager.current_menu = "awaiting_new_collection_name"
                
            
                elif command == '4':
                    
                    emit('execute_command_response', {
                        'output': '\n<h2>Please enter the collection name to delete:</h2>',
                        'raw_output': ''
                    })
                    
                    menu_manager.current_menu = "awaiting_collection_to_delete"
                
            
                elif command == '5':
                    try:
                    
                        documents = list(menu_manager.collection_in_use.find({}))
                    
                        remote_response = json_util.dumps(documents, indent=2)
                    
                        emit('execute_command_response', {
                            'output': f'\n<strong>Documents: <h3>{remote_response}</h3></strong>\n' + menu_manager.get_collection_menu(),
                            'raw_output': capturing_Atlas(documents)
                        })
                    
                    except Exception as e:
                    
                        emit('execute_command_response', {
                            'output': f'\n<h3>Error executing query: {str(e)}</h3>',
                            'raw_output': capturing_Atlas(str(e))
                        })
                
                elif command == '6':
                    
                    emit('execute_command_response', {
                        'output': '\n<h2>Please enter the query (JSON format).\nType "EOF" on a new line to submit.</h2>',
                        'raw_output': ''
                    })
                    
                    menu_manager.current_menu = "awaiting_find_one"
                
            
                elif command == '7':
                    
                    emit('execute_command_response', {
                        'output': '\n<h2>Please enter the document to insert (JSON format).\nType "EOF" on a new line to submit.</h2>',
                        'raw_output': ''
                    })
                    
                    menu_manager.current_menu = "awaiting_insert_one"
                
                elif command == '8':
                    
                    emit('execute_command_response', {
                        'output': '\n<h2>Please enter the list of documents to insert (JSON format).\nType "EOF" on a new line to submit.</h2>',
                        'raw_output': ''
                    })
                    
                    menu_manager.current_menu = "awaiting_insert_many"
                
                elif command == '9':
                    
                    emit('execute_command_response', {
                        'output': '\n<h2>Please enter the filter query (JSON format).\nType "EOF" on a new line to submit.</h2>',
                        'raw_output': ''
                    })
                    
                    menu_manager.current_menu = "awaiting_update_one"
                
                elif command == '10':
                    
                    emit('execute_command_response', {
                        'output': '\n<h2>Please enter the delete query (JSON format).\nType "EOF" on a new line to submit.</h2>',
                        'raw_output': ''
                    })
                    
                    menu_manager.current_menu = "awaiting_delete_one"
                
                elif command == '11':
                    
                    menu_manager.current_menu = "database_menu"
                    
                    emit('execute_command_response', {
                        'output': menu_manager.get_database_menu(),
                        'raw_output': ''
                    })
                
                elif command in ['menu', 'clear', 'help', 'exit']:
    
                    response = menu_comunes.comunes(command)
                   
                    if response:
                        emit('execute_command_response', response)
                
                else:
                
                    emit('execute_command_response', {
                        'output': '\n<h3>Input error. Please Type "menu" to see options, "clear" to clear the screen, and "exit" to exit.</h3>',
                        'raw_output': ''
                    })

            elif menu_manager.current_menu == "awaiting_collection_name":
                
                collection_name = command.strip()
                
                if collection_name:
                
                    try:
                        
                        collections = menu_manager.db_in_use.list_collection_names()
                
                        if collection_name in collections:
                
                            menu_manager.collection_in_use = menu_manager.db_in_use[collection_name]
                        
                            menu_manager.current_menu = "collection_menu"
                
                            emit('execute_command_response', {
                                'output': f'\n<h2>Using collection: {collection_name}</h2>\n' + menu_manager.get_collection_menu(),
                                'raw_output': capturing_Atlas(collection_name)
                            })
                        
                        else:
                
                            emit('execute_command_response', {
                                'output': f'\n<h3>Error: Collection "{collection_name}" does not exist.</h3>\n' + menu_manager.get_collection_menu(),
                                'raw_output': capturing_Atlas(f'Collection "{collection_name}" does not exist.')
                            })
                
                            menu_manager.current_menu = "collection_menu"
                    
                    except Exception as e:
                
                        emit('execute_command_response', {
                            'output': f'\n<h3>Error selecting collection: {str(e)}</h3>',
                            'raw_output': capturing_Atlas(str(e))
                        })
                
                        menu_manager.current_menu = "collection_menu"
                
                else:
                
                    emit('execute_command_response', {
                        'output': '\n<h3>Error: Collection name not provided.</h3>\n' + menu_manager.get_collection_menu(),
                        'raw_output': capturing_Atlas('Collection name not provided.')
                    })
                
                    menu_manager.current_menu = "collection_menu"

            elif menu_manager.current_menu == "awaiting_new_collection_name":
                
                collection_name = command.strip()
                
                if collection_name:
                
                    try:
                
                        menu_manager.db_in_use.create_collection(collection_name)
                        
                        menu_manager.collection_in_use = menu_manager.db_in_use[collection_name]
                        
                        menu_manager.current_menu = "collection_menu"
                
                        emit('execute_command_response', {
                            'output': f'\n<h2>Collection \'{collection_name}\' created.</h2>\n' + menu_manager.get_collection_menu(),
                            'raw_output': capturing_Atlas(collection_name)
                        })
                    
                    except Exception as e:
                
                        emit('execute_command_response', {
                            'output': f'\n<h3>Error creating collection: {str(e)}</h3>',
                            'raw_output': capturing_Atlas(str(e))
                        })
                
                        menu_manager.current_menu = "collection_menu"
                
                else:
                
                    emit('execute_command_response', {
                        'output': '\n<h3>Error: Collection name not provided.</h3>\n' + menu_manager.get_collection_menu(),
                        'raw_output': capturing_Atlas('Collection name not provided.')
                    })
                
                    menu_manager.current_menu = "collection_menu"

            elif menu_manager.current_menu == "awaiting_collection_to_delete":
                
                collection_name = command.strip()
                
                if collection_name:
                    
                    confirm = data.get('confirm', '').strip()
                    
                    if confirm == 'YES':
                        
                        try:
                        
                            menu_manager.db_in_use.drop_collection(collection_name)
                        
                            emit('execute_command_response', {
                                'output': f'\n<h2>Collection \'{collection_name}\' deleted.</h2>\n' + menu_manager.get_collection_menu(),
                                'raw_output': capturing_Atlas(f'Collection "{collection_name}" deleted.')
                            })
                        
                        except Exception as e:
                        
                            emit('execute_command_response', {
                                'output': f'\n<h3>Error deleting collection: {str(e)}</h3>',
                                'raw_output': capturing_Atlas(str(e))
                            })
                    
                    else:
                        
                        emit('execute_command_response', {
                            'output': '\n<h2>Deletion canceled.</h2>\n' + menu_manager.get_collection_menu(),
                            'raw_output': capturing_Atlas('Deletion canceled.')
                        })
                    
                    menu_manager.current_menu = "collection_menu"    
                            
                else:
                    
                    emit('execute_command_response', {
                        'output': '\n<h3>Error: Collection name not provided.</h3>\n' + menu_manager.get_collection_menu(),
                        'raw_output': capturing_Atlas('Collection name not provided.')
                    })
                    
                    menu_manager.current_menu = "collection_menu"

            elif menu_manager.current_menu in [
                
                "awaiting_find_all",
                "awaiting_find_one",
                "awaiting_insert_one",
                "awaiting_insert_many",
                "awaiting_update_one",
                "awaiting_delete_one"
                
                ]:
                
                if command.strip().upper() == 'EOF':
                    
                    try:
                        
                        json_as_dict = process_json_input(data.get('json_lines', []))

                        if menu_manager.current_menu == "awaiting_find_all":
                            
                            documents = list(menu_manager.collection_in_use.find({}))
                            
                            remote_response = json_util.dumps(documents, indent=2)
                            
                            emit('execute_command_response', {
                                'output': f'\n<strong>Documents: <h3>{remote_response}</h3></strong>\n' + menu_manager.get_collection_menu(),
                                'raw_output': capturing_Atlas(documents)
                            })

                        elif menu_manager.current_menu == "awaiting_find_one":
                            
                            document = menu_manager.collection_in_use.find_one(json_as_dict)
                            
                            remote_response = json_util.dumps(document, indent=2)
                            
                            emit('execute_command_response', {
                                'output': f'\n<strong>Document: <h3>{remote_response}</h3></strong>\n' + menu_manager.get_collection_menu(),
                                'raw_output': capturing_Atlas(document)
                            })

                        elif menu_manager.current_menu == "awaiting_insert_one":
                            
                            result = menu_manager.collection_in_use.insert_one(json_as_dict)
                            
                        
                            emit('execute_command_response', {
                                'output': f'\n<h2>Document inserted with ID: {result.inserted_id}</h2>\n' + menu_manager.get_collection_menu(),
                                'raw_output': capturing_Atlas(result.inserted_id)
                            })

                        elif menu_manager.current_menu == "awaiting_insert_many":
                            
                            result = menu_manager.collection_in_use.insert_many(json_as_dict)
                            
                            emit('execute_command_response', {
                                'output': f'\n<h2>{len(result.inserted_ids)} documents inserted.</h2>\n' + menu_manager.get_collection_menu(),
                                'raw_output': capturing_Atlas(result.inserted_ids)
                            })

                        elif menu_manager.current_menu == "awaiting_update_one":
                            
                            filter_query = json_as_dict.get('filter', {})
                            
                            update_query = json_as_dict.get('update', {})
                            
                            result = menu_manager.collection_in_use.update_one(filter_query, update_query)
                            
                            emit('execute_command_response', {
                                'output': f'\n<h2>Matched {result.matched_count} document(s) and modified {result.modified_count} document(s).</h2>\n' + menu_manager.get_collection_menu(),
                                'raw_output': capturing_Atlas({
                                    'matched_count': result.matched_count,
                                    'modified_count': result.modified_count
                                })
                            })

                        elif menu_manager.current_menu == "awaiting_delete_one":
                            
                            result = menu_manager.collection_in_use.delete_one(json_as_dict)
                            
                            emit('execute_command_response', {
                                'output': f'\n<h2>Deleted {result.deleted_count} document(s).</h2>\n' + menu_manager.get_collection_menu(),
                                'raw_output': capturing_Atlas(result.deleted_count)
                            })

                    except ValueError as e:

                        emit('execute_command_response', {
                            'output': f'\n<h3>Error processing JSON: {str(e)}</h3>',
                            'raw_output': capturing_Atlas(str(e))
                        })
                    
                    finally:
                        
                        data['json_lines'] = []
                        
                        menu_manager.current_menu = "collection_menu"
                
                else:

                    if 'json_lines' not in data:

                        data['json_lines'] = []
                
                    data['json_lines'].append(command)
                
                    emit('execute_command_response', {
                        'output': command,
                        'raw_output': ''
                    })

        except Exception as e:
            
            print(f'>> DEBUG: Error in socketio_commander: {str(e)}')
            
            emit('execute_command_response', {
                'output': f'\n<h3>Error: {str(e)}</h3>',
                'raw_output': capturing_Atlas(str(e))
            })