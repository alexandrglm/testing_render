################################################################################
# Project 13: Scrappy v0.1
#
# Concept:  Advanced Web Content Scraper with Markdown Exporter 
################################################################################
"""
This concept provides an advanced web content scraper that convertsany "text-ible" data
into Markdown documents. It includes features for:

1.  Exclusion Filters: Removing duplicate content using regular expressions (REGEX).
2.  Content Mappers: Transforming HTML elements (specific div class/id's) into regular Markdown styles.
3.  MongoDB as persistance Storage for filters' rulesets and documents.
"""
################################################################################
# PENDING:
"""
A lot of corrections, improvements, fixes, pending:

- Refactorinf and simplifying:
   * The filters part: Multi-line inputs directly pasted instead of line1\nline2\n
   * JSON/BJSON Ruleset/Documents handler into ONE CLASS! (The more repited code structures)

- Conversions have to be made using PANDOC instead of bs4/html2text

- ACE9 markdown: Configs

"""
################################################################################
# Imports
################
from flask import Blueprint, render_template, request, jsonify, current_app
import os
import json
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import html2text
import re
import time
################################################################################
# Setenvs and vars
################
project13 = Blueprint('project13', __name__)

load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS')
MONGO_HOST_1 = os.getenv('MONGO_HOST_1')
MONGO_HOST_2 = os.getenv('MONGO_HOST_2')
MONGO_HOST_3 = os.getenv('MONGO_HOST_3')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_SETS = os.getenv('MONGO_SETS')

PROJECT13_DB = os.getenv('PROJECT13_DB')
PROJECT13_FILTERS = os.getenv('PROJECT13_FILTERS')
PROJECT13_PAGES = os.getenv('PROJECT13_PAGES')

MONGO_URI = f'mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST_1}:{MONGO_PORT},{MONGO_HOST_2}:{MONGO_PORT},{MONGO_HOST_3}:{MONGO_PORT}/?replicaSet={MONGO_SETS}'


SCRAPER_OPTIONS = {
    'scroll': {
        'label': 'Scroll page',
        'description': 'Load dynamic content',
        'default': True
    },
    'wait_for_element': {
        'label': 'Wait for element (CSS)',
        'description': 'Optional CSS selector',
        'default': ''
    }
}

clean_tags = ['script', 'style', 'noscript', 'svg', 'form', 'iframe']


LOCAL_RULESETS = os.listdir('data/13/filtersmappers')
LOCAL_DOCS = os.path.join(os.path.dirname(__file__), 'data/13/uploads')


################################################################################
# debug logger
################
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

################################################################################
# 
################
class ScrappyLogics:

    def __init__(self, headless=True, wait_time=10, output_dir=None, template_name='default'):
        self.headless = headless
        self.wait_time = wait_time
        self.output_dir = output_dir or LOCAL_DOCS
        self.template_name = template_name
        self.driver = None
        self.custom_mappings = {}
        self.exclusion_patterns = []
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs('templates', exist_ok=True)
        
        self._load_template()
        self._init_driver()
        logging.info('Scraper initialized')

    def _get_mongo_client(self):
        
        try:
        
            return MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=30000,
                socketTimeoutMS=30000
            )
        
        
        except Exception as e:
        
            logging.warning(f'MongoDB connection failed: {str(e)}')
            return None

    def _load_template(self):
        
        #########################################################################################
        # 1st MONGO ATLAS
        #########################################################################################
        mongo_client = self._get_mongo_client()


        if mongo_client:
    
            try:
    
                db = mongo_client[PROJECT13_DB]
                template = db[PROJECT13_FILTERS].find_one({'name': self.template_name})
                
                if template:
    
                    self.custom_mappings = template.get('element_mappings', {})
                    self.exclusion_patterns = template.get('exclusion_patterns', [])
                    logging.info(f'Using MongoDB template: {self.template_name}')
                    return
            
            except Exception as e:
            
                logging.warning(f'MongoDB template load error: {str(e)}')
            
            finally:
            
                mongo_client.close()

        
        #########################################################################################
        # 2nd LOCAL FALLBACK WHEN MONGO ATLAS ISN'T AVAILABLE
        #########################################################################################
        template_path = os.path.join('data/13/filtersmappers', f'{self.template_name}.json')
        
        if os.path.exists(template_path):
        
            try:
        
                with open(template_path, 'r', encoding='utf-8') as f:
        
                    config = json.load(f)
                    self.custom_mappings = config.get('element_mappings', {})
                    self.exclusion_patterns = config.get('exclusion_patterns', [])
        
                    logging.info(f'Using local JSON template: {self.template_name}')
        
            except Exception as e:
        
                logging.error(f'Local template load error: {str(e)}')
        
        else:
        
            logging.info('Using default configuration')

    # SELENIUM CONFIGS
    def _init_driver(self):
    
        chrome_options = Options()
    
        if self.headless:
        
            chrome_options.add_argument("--headless=new")
        
        
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
        
            self.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        
        
        except Exception as e:
        
            logging.error(f'Chrome driver init failed: {str(e)}')
            raise




    def scrape_page(self, url, scroll=False, wait_for_element=None):
        
        logging.info(f'Fetching: {url}')
        
        
        try:
        
            # URI vlaidation
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            self.driver.get(url)

            WebDriverWait(self.driver, self.wait_time).until(
                
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )

            
            if wait_for_element:
            
                try:
            
                    WebDriverWait(self.driver, self.wait_time).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_element)))
            
                except Exception as e:
            
                    logging.warning(f'Timeout waiting for element {wait_for_element}: {str(e)}')

            if scroll:
                self._scroll_page()

            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            self._apply_html_filters(soup)
            
            
            for tag in clean_tags:
            
                [x.decompose() for x in soup(tag)]
            
            title = soup.title.string if soup.title else urlparse(url).netloc
            
            h = html2text.HTML2Text()
            h.body_width = 0
            h.mark_code = True
            h.wrap_list_items = True
            h.ul_item_mark = '-'
            h.emphasis_mark = '*'
            h.strong_mark = '**'
            
            markdown_content = h.handle(str(soup.body)) if soup.body else ""

            if self.exclusion_patterns:
            
                markdown_content = self._apply_markdown_exclusions(markdown_content)
            
            
            
            return {
                'title': title,
                'url': url,
                'content': markdown_content,
                'timestamp': datetime.now().isoformat()
            }
        
        
        except Exception as e:
        
            logging.error(f'Scraping failed: {str(e)}')
            raise
        
        
        finally:
            logging.info('Scraping completed')

    


    def _scroll_page(self):
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
        
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        
            time.sleep(2)
        
            new_height = self.driver.execute_script("return document.body.scrollHeight")
        
            if new_height == last_height:
                break
        
            last_height = new_height

    

    def _apply_html_filters(self, soup):
        
        for selector, md_type in self.custom_mappings.items():
        
            try:
        
                elements = soup.select(selector)
        
                for element in elements:
        
                    if md_type.startswith('h'):
                        element.name = md_type
        
                    elif md_type == 'bold':
                        element.wrap(soup.new_tag('strong'))
        
                    elif md_type == 'italic':
                        element.wrap(soup.new_tag('em'))
        
                    elif md_type == 'code':
                        element.wrap(soup.new_tag('code'))
        
            except Exception as e:
                
                logging.warning(f'Error applying filter {selector}: {str(e)}')

    

    def _apply_markdown_exclusions(self, content):
        
        if not self.exclusion_patterns:
        
            return content

        lines = content.split('\n')
        filtered_lines = []
        i = 0
        
        while i < len(lines):
        
            line = lines[i]
        
            exclude = False
            
            for pattern in self.exclusion_patterns:
        
                # BASIC / ADVANCED inputs
        
                if isinstance(pattern, dict):

                    # BASIC mode
                    if 'is_regex' in pattern and not pattern['is_regex']:
                        
                        try:

                            regex_pattern = re.escape(pattern['raw'])

                            regex_pattern = regex_pattern.replace(r'\*', '.*?')

                            if re.fullmatch(regex_pattern, line.strip()):

                                exclude = True
                                break

                        except re.error:

                            logging.warning(f"Invalid generated regex from BASIC pattern: {pattern['raw']}")
                            continue
                    
                    # ADVANCED mode
                    elif 'raw' in pattern:
                        try:
                            if re.fullmatch(pattern['raw'], line.strip()):
                                exclude = True
                                break
                        except re.error:
                            logging.warning(f"Invalid ADVANCED regex pattern: {pattern['raw']}")
                            continue
                
                # REHACER parte 1
                elif 'lines' in pattern:

                    pattern_lines = pattern['lines']
                    match = True
                    
                    for j in range(len(pattern_lines)):
                        
                        if i + j >= len(lines) or lines[i + j].rstrip() != pattern_lines[j].rstrip():
                            
                            match = False
                            break
                    
                    if match:
                        
                        exclude = True
                        i += len(pattern_lines) - 1
                        break
            
            
            if not exclude:
                
                filtered_lines.append(line)
            
            i += 1
        
        return '\n'.join(filtered_lines)



    def save_to_markdown(self, data, filename=None):
    
        if not filename:
    
            filename = f"{self._sanitize_filename(data['title'])}.md"
        
    
        filepath = os.path.join(self.output_dir, filename)
        
    
        try:
    
            with open(filepath, 'w', encoding='utf-8') as f:
    
                f.write(f"# {data['title']}\n\n")
                f.write(f"**URL:** {data['url']}\n")
                f.write(f"**Scraped:** {data['timestamp']}\n\n")
                f.write(data['content'])
            
    
            logging.info(f'File saved: {filepath}')
            return filepath
        
        except Exception as e:
    
            logging.error(f'Error saving file: {str(e)}')
            raise




    def _sanitize_filename(self, text):
    
        return re.sub(r'[<>:"/\\|?*]', '_', text)[:100]




    def close(self):
    
        if self.driver:
            self.driver.quit()



    def __del__(self):
        self.close()


################
# Mongo basico
def get_mongo_client():
    
    try:
    
        return MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000
        )
    
    except Exception as e:
    
        logging.error(f"MongoDB connection error: {str(e)}")
        return None

################################################################################
# Routes:
################
# 1 MAIN
################
@project13.route('/')
def render_project_13():
    return render_template('13/index_13.html', scraper_options=SCRAPER_OPTIONS)
################
# 2 FILTERS TEMPLATES
################
@project13.route('/filtersmappers/')

def list_templates():

    templates = ['default']


    #########################################################################################
    # 1st MONGO ATLAS
    ################
    mongo_client = get_mongo_client()
    
    if mongo_client:

        try:

            db = mongo_client[PROJECT13_DB]
            templates_cursor = db[PROJECT13_FILTERS].find({}, {'name': 1})
            templates.extend([t['name'] for t in templates_cursor])

        except Exception as e:
            logging.error(f"MongoDB template list error: {str(e)}")

        finally:
            mongo_client.close()
    

    #########################################################################################
    # 2nd LOCAL FALLBACK WHEN MONGO ATLAS ISN'T AVAILABLE
    ################
    try:
    
        local_templates = [f.replace('.json', '') for f in LOCAL_RULESETS if f.endswith('.json')]
        templates.extend(local_templates)
    
    except Exception as e:
    
        logging.error(f"Local template list error: {str(e)}")
    
    return jsonify({"templates": list(set(templates))})
################
# 3 WEB SCRAPER
################
@project13.route('/scrappy', methods=['POST'])
def scrappy_url():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # REHACERLO parte 2
        if 'filters' in data and 'exclusionPatterns' in data['filters']:

            processed_exclusions = []

            for pattern in data['filters']['exclusionPatterns']:

                if isinstance(pattern, dict) and 'raw' in pattern:

                    # Raw es raw, debug y mostrar
                    # True para Advanced, False para Basic
                    processed_exclusions.append({
                        'raw': pattern['raw'],
                        'is_regex': pattern.get('is_regex', False) 
                    })
                
                else:

                    # REHACER parte 3
                    processed_exclusions.append({
                        'lines': pattern['raw'].split('\n') if 'raw' in pattern else pattern.split('\n'),
                        'is_regex': False
                    })
            
            data['filters']['exclusionPatterns'] = processed_exclusions

        scraper = ScrappyLogics(
            headless=True,
            wait_time=10,
            output_dir=LOCAL_DOCS,
            template_name=data.get('template', 'default')
        )
        
        if data.get('filters'):
        
            scraper.custom_mappings = data['filters'].get('elementMappings', {})
            scraper.exclusion_patterns = data['filters'].get('exclusionPatterns', [])
        
        scraped_data = scraper.scrape_page(
            data['url'],
            scroll=data.get('options', {}).get('scroll', False),
            wait_for_element=data.get('options', {}).get('wait_for_element')
        )
        
        #########################################################################################
        # 1st MONGO ATLAS
        ################
        mongo_client = get_mongo_client()
        
        if mongo_client:
        
            try:
        
                db = mongo_client[PROJECT13_DB]
        
                db[PROJECT13_PAGES].insert_one({
                    'title': scraped_data['title'],
                    'url': scraped_data['url'],
                    'content': scraped_data['content'],
                    'filters': data.get('filters', {}),
                    'timestamp': scraped_data['timestamp']
                })
        
        
            except Exception as e:
        
                logging.error(f"MongoDB save error: {str(e)}")
        
        
            finally:
        
                mongo_client.close()
        

        #########################################################################################
        # SAving file using Atlas as persistant storage
        ##############
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{scraper._sanitize_filename(scraped_data['title'])}_{timestamp}.md"
        filepath = scraper.save_to_markdown(scraped_data, filename)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'markdown': scraped_data['content'],
            'metadata': {
                'title': scraped_data['title'],
                'url': scraped_data['url'],
                'timestamp': scraped_data['timestamp']
            }
        })
        
    
    except Exception as e:
    
        logging.error(f"Error scraping: {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500
    
    
    finally:
    
        if 'scraper' in locals():
            scraper.close()

################
# 4 FILTER TEMPLATES SINGLE LOADER
################
@project13.route('/mapper/<name>')
def get_template(name):
   
    template_data = {
        'element_mappings': {},
        'exclusion_patterns': [],
        'description': ''
    }
    

    #########################################################################################
    # 1st MONGO ATLAS
    ################
    mongo_client = get_mongo_client()
   
    if mongo_client:
   
        try:
   
            db = mongo_client[PROJECT13_DB]
            template = db[PROJECT13_FILTERS].find_one({'name': name})
   
            if template:
   
                template_data.update({
                    'element_mappings': template.get('element_mappings', {}),
                    'exclusion_patterns': template.get('exclusion_patterns', []),
                    'description': template.get('description', '')
                })
   
   
        except Exception as e:
            logging.error(f"MongoDB template load error: {str(e)}")
   
   
        finally:
            mongo_client.close()
    
    #########################################################################################
    # 2nd LOCAL FALLBACK WHEN MONGO ATLAS ISN'T AVAILABLE
    ################
   
    template_path = (LOCAL_RULESETS, f'{name}.json')

    if os.path.exists(template_path):

        try:

            with open(template_path, 'r') as f:

                local_data = json.load(f)

                template_data.update({
                    'element_mappings': local_data.get('element_mappings', {}),
                    'exclusion_patterns': local_data.get('exclusion_patterns', [])
                })

        except Exception as e:
            logging.error(f"Local template load error: {str(e)}")
    
    return jsonify(template_data)
################
# SAVE CUSTOM FILTERS
################
@project13.route('/save-template', methods=['POST'])
def save_template():
    
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'success': False, 'error': 'Template name is required'}), 400
    
    success = False

    #########################################################################################
    # 1st MONGO ATLAS
    ################
    mongo_client = get_mongo_client()
    
    if mongo_client:
    
        try:
    
            db = mongo_client[PROJECT13_DB]
    
            result = db[PROJECT13_FILTERS].update_one(
                {'name': data['name']},
                {'$set': {
                    'element_mappings': data.get('filters', {}).get('elementMappings', {}),
                    'exclusion_patterns': data.get('filters', {}).get('exclusionPatterns', []),
                    'description': data.get('description', ''),
                    'last_modified': datetime.now().isoformat()
                }},
                upsert=True
            )
    
            success = True
    
    
        except Exception as e:
    
            logging.error(f"MongoDB template save error: {str(e)}")
    
    
        finally:
            mongo_client.close()
    
    #########################################################################################
    # 2nd LOCAL FALLBACK WHEN MONGO ATLAS ISN'T AVAILABLE
    ################
    try:

        template_path = (LOCAL_RULESETS, f"{data['name']}.json")

        with open(template_path, 'w') as f:
            json.dump({
                'element_mappings': data.get('filters', {}).get('elementMappings', {}),
                'exclusion_patterns': data.get('filters', {}).get('exclusionPatterns', []),
                'description': data.get('description', ''),
                'last_modified': datetime.now().isoformat()
            }, f, indent=2)
        success = True

    except Exception as e:

        logging.error(f"Local template save error: {str(e)}")
    
    return jsonify({'success': success})