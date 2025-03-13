############################################################################
# Project 09: MarkDown Web Server
#
# A web MarkDown files renderer framework.
################
# Imports
from flask import Flask, Blueprint, render_template, request, send_from_directory
import os
import re
from markupsafe import Markup
import markdown
################
# 9.1 Main vars
library_dir = os.path.join(os.path.dirname(__file__), 'data/09/library')
# Blueprint app route for 09
project09 = Blueprint('project09', __name__)
##################
@project09.route('/')
def render_project_09():
    library_index = []

    for root, dirs, files in os.walk(library_dir):
        
        rel_path = os.path.relpath(root, library_dir)
        rel_path = "" if rel_path == "." else rel_path
        library_index.append((rel_path, dirs, files))

    return render_template(
        '09/index_09.html',
        library_index=library_index,
        library_dir=library_dir
    )
##################
# Parsing MD -> IMG Serving = PostProcess html to replace img routes
@project09.route('/data/09/library/<path:filename>')
def parse_markdown(file_path):

    if not os.path.exists(file_path):
        
        return render_template('404/index_404.html')

    try:

        with open(file_path, 'r', encoding='UTF-8') as f:
            md_content = f.read()

        html_content = markdown.markdown(
            md_content,
            extensions=[
                'extra',
                'tables',
                'fenced_code',
                'toc',
                'md_in_html',
                'attr_list',
                'pymdownx.arithmatex',
            ],
            extension_configs={
                'pymdownx.arithmatex': {
                    'generic': True,
                }
            }
        )

        html_content = postprocess_html(html_content, os.path.dirname(file_path))
        return html_content
    
    except Exception as e:

        print(f"Error al procesar Markdown: {e}")
        return None

def serve_image(filename):
    directory = os.path.abspath(os.path.join(os.getcwd(), "data", "09", "library"))
    
    if not os.path.exists(os.path.join(directory, filename)):
        filename = ''
        return "Imagen no encontrada", 404
    
    return send_from_directory(directory, filename)

def postprocess_html(html_content, md_directory):
    img_pattern = re.compile(r'<img[^>]+src="([^"]+)"', re.IGNORECASE)
    
    def replace_img_src(match):
        src = match.group(1)

        if not src.startswith(('http://', 'https://')):
            
            src = src.lstrip('./')
            new_src = f"/09/data/09/library/{os.path.relpath(os.path.join(md_directory, src), start=library_dir)}"
            
            return match.group(0).replace(match.group(1), new_src)
        
        return match.group(0)
    
    return img_pattern.sub(replace_img_src, html_content)
##################
# Renders
@project09.route('/render/<filename>')
def rendering_md(filename):

    sanitized_filename = pre_sanitize_filenames(filename)
    file_path = None

    for root, _, files in os.walk(library_dir):

        for md_file in files:

            if pre_sanitize_filenames(md_file) == sanitized_filename and md_file.endswith(('.md', '.markdown')):
                file_path = os.path.join(root, md_file)
                break

        if file_path:
            break

    if not file_path:
        return render_template('404/index_404.html')

    html_content = parse_markdown(file_path)

    if not html_content:
        return render_template('404/index_404.html')

    page_title = Titleized_names(filename)

    return render_template(
        '09/template.html',
        content=html_content,
        page_title=page_title,
        md_directory=os.path.dirname(file_path)
    )
##################
# Filename Pre-sanitization
def pre_sanitize_filenames(name):
    
    base_name, extension = os.path.splitext(name)
    sanitized = re.sub(r'[^\w\s-]', '', base_name)
    sanitized = re.sub(r'[-\s]+', '-', sanitized).strip('-')
    
    if '..' in sanitized or '/' in sanitized or '\\' in sanitized:
        raise ValueError("DEBUG: File PRE sanitization failed")
    
    return sanitized
##################
# Index titles' formatter
def Titleized_names(name):

    base_name, _ = os.path.splitext(name)
    formatted = re.sub(r'[-_]', ' ', base_name)

    return formatted.title()