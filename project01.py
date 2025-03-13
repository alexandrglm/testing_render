############################################################################
# Project 01: A "simple" HelloWorld using Flask
from flask import Blueprint, render_template

############################################################################
# 01 logic
###############
# app.route to Blueprint:
project01 = Blueprint('project01', __name__)
###############
# 01 main
@project01.route('/')
def render_project_01():
    
    heading = Headings('Zero Front-end drama')
    
    p1 = P('No HTML or CSS files were harmed in the making of this Hello World screen.', style="font-style:italic;")
    p2 = P('Hello World, by the way.')
    
    heading_4 = Headings('This is how this hello world page is build', heading_type=4)
    
    footer = Footer()

    code_content = '''

# Enjoy reading code
def render():

    heading = Headings('Zero Front-end drama')
    p1 = P('No HTML or CSS were harmed in the making of this Hello World screen.', style="font-style:italic;")
    p2 = P('Hello World, by the way.')

    code_content = Code to be shown, here
    code_style = "font-style:italic; background-color:lightgray;"

    # Web Builders
    site = Site(title='title', web_elements=[])
    site.joining_web_elements(heading)
    site.joining_web_elements(p1)
    site.joining_web_elements(p2)
    site.joining_web_elements(Code(code_content, code_style))

    # Render start
    return site.render_html()

# Now, Class'es
# The Parent Class
class HtmlRender:
    def __init__(self, content):
        self.content = content

    def render_html(self):
        raise NotImplementedError('DEBUG: No está recogiendo el contenido')


# Body COntent Classes as Child Classes

class Headings(HtmlRender):
    def __init__(self, content, heading_type=1):
        super().__init__(content)
        self.heading_type = heading_type

    def render_html(self):
        return f'< h{ self.heading_type} >{ self.content}< /h{ self.heading_type} >'

    
class P(HtmlRender):
    def __init__(self, content, style=None):
        super().__init__(content)
        self.style = style

    def render_html(self):
        if self.style:
            return f'< p style="{ self.style}">< /p>'
        return f'< p >{ self.content}< /p >'

# How this code block is being projected
class Code(HtmlRender):
    def __init__(self, content, style="font-style:italic; background-color:lightgray;"):
        super().__init__(content)
        self.style = style

    def render_html(self):
        return f'< pre >< code style="{ self.style}">{ self.content}< /code >< /pre >'


# How this site is being build
class Site(HtmlRender):
    def __init__(self, title, web_elements=None):
        super().__init__('')
        self.title = title
        self.web_elements = web_elements if web_elements is not None else []

    def joining_web_elements(self, single_element):
        self.web_elements.append(single_element)

    def render_html(self):
        body_wrapped = ''
        
        for single_element in self.web_elements:
            body_wrapped += single_element.render_html() + '\\n'

        return f' ' '
< html >
    < head >
        < title >{self.title}< /title >
    < /head >
    < body >
        {body_wrapped}
    < /body >
< /html >' ' ' '''

    code_style = "font-style:italic;"

    
    # BUilding the web
    site = HelloWorldPage(title='Project 01: The most complex "Simple Hello World" site', web_elements=[])
    site.joining_web_elements(heading)
    site.joining_web_elements(p1)
    site.joining_web_elements(heading_4)
    site.joining_web_elements(Code(code_content, code_style))
    site.joining_web_elements(p2)
    site.joining_web_elements(footer)
    

    # Rendering 
    return site.render_html()

class HtmlRender:
    def __init__(self, content):
        self.content = content

    def render_html(self):
        raise NotImplementedError('DEBUG: No está recogiendo el contenido')

class Headings(HtmlRender):
    def __init__(self, content, heading_type=1):
        super().__init__(content)
        self.heading_type = heading_type

    def render_html(self):
        return f'<h{self.heading_type}>{self.content}</h{self.heading_type}>'

class P(HtmlRender):
    def __init__(self, content, style=None):
        super().__init__(content)
        self.style = style

    def render_html(self):
        if self.style:
            return f'<p style="{self.style}">{self.content}</p>'
        return f'<p>{self.content}</p>'

class Code(HtmlRender):
    def __init__(self, content, style="font-style:italic; background-color:lightgray;"):
        super().__init__(content)
        self.style = style

    def render_html(self):
        return f'<pre><code style="{self.style}">{self.content}</code></pre>'

class Footer(HtmlRender):
    def __init__(self):
        super().__init__('')

    def render_html(self):
        return render_template('_footer.html')

class HelloWorldPage(HtmlRender):
    def __init__(self, title, web_elements=None):
        super().__init__('')
        self.title = title
        self.web_elements = web_elements if web_elements is not None else []

    def joining_web_elements(self, single_element):
        self.web_elements.append(single_element)

    def render_html(self):
        body_wrapped = ''
        
        for single_element in self.web_elements:
            body_wrapped += single_element.render_html() + '\n'

        return f'''<!DOCTYPE html>
<html>
    <head>
        <title>{self.title}</title>
    </head>
    <body>
        {body_wrapped}
    </body>
</html>'''

