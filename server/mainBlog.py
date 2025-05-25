
from server.mainObjects import projects
from server.main import rendering_checks
import os
from flask import Flask, render_template, send_from_directory, request, jsonify
from markupsafe import Markup
from datetime import datetime
import markdown

###############
# Posts
def start_blog(app):

    @app.route('/blog/<int:year>/<int:month>/<slug>/')
    def render_blog(year, month, slug):

        # metadata.link + metadata.YYYY--metadata-MM
        blog = next((p for p in projects
                    if p.get('type') == 'blog'
                    and p.get('metadata', {}).get('link') == slug
                    and p.get('metadata', {}).get('date', '').startswith(f'{year}-{month:02d}')), None)

        # Pending checks, might be duplicated as Exception does
        if not blog:

            return render_template('404/index_404.html')


        try:

            template_path = f'blog/{year}/{month:02d}/{slug}.html'
            return render_template(template_path, blog=blog)

        except Exception as e:

            print(f'\n[ERROR] (BLOGS) -> {template_path} error :\n   {str(e)}\n\n')
            return render_template('404/index_404.html')



    def main_blog_snapshot(project):
        metadata = project.get('metadata', {})
        snapshot = metadata.get('snapshot', '').strip()

        if snapshot:

            date = metadata.get('date', '')
            link = metadata.get('link', 'default')
            
            try:
                year, month, *_ = date.split('-')
                filename = f"blog/{year}/{month}/{link}/{snapshot}"
                return send_from_directory('static', filename)
            
            except ValueError:
                pass

        return send_from_directory('static/blog', 'blog-default.png')



    def markdown_to_blog(projects):

        for post in projects:
            
            if post.get('type') != 'blog':
                continue

            meta = post.get('metadata', {})
            date = meta.get('date')
            link = meta.get('link')

            if not (date and link):
                continue

            try:

                dt = datetime.strptime(date, '%Y-%m-%d')
                yyyy = dt.strftime('%Y')
                mm = dt.strftime('%m')
            
            except ValueError:
                
                print(f'\n\n[ERROR] (BLOG) -> Missing DATE/LINK in {entry}! : {str(ValueError)}')
                continue

            
            md_filename = f'{date}_{link}.md'

            md_path = os.path.join('data', 'blog', md_filename)

            if not os.path.exists(md_path):
                
                continue

            
            template_path = os.path.join('data', 'blog', 'BLOG_template.html')
            
            if not os.path.exists(template_path):
                continue

            
            with open(md_path, "r", encoding="utf-8") as f:
                
                md_content = f.read()

            
            html_body = markdown.markdown(md_content, extensions=["extra", "fenced_code", "codehilite", "toc", "attr_list"])

            
            with open(template_path, "r", encoding="utf-8") as f:
                
                base_template = f.read()

            
            
            post_html = base_template.replace("{{ content }}", html_body)

            blog_paths = os.path.join('templates', "blog", yyyy, mm)
            os.makedirs(blog_paths, exist_ok=True)

            out_path = os.path.join(blog_paths, f'{link}.html')

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(post_html)

    rendering_checks()
    markdown_to_blog(projects)
