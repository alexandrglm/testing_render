
############################################################################
# 10 MarkDown onto webs
############################################################################

# Configuración del catálogo
md_catalog = './data/10/md_catalog/'

# Función para sanitizar nombres de archivo
def sanitize_filename(name):
    base_name, extension = os.path.splitext(name)
    sanitized = re.sub(r'[^\w\s-]', '', base_name)
    sanitized = re.sub(r'[-\s]+', '-', sanitized).strip('-')
    if '..' in sanitized or '/' in sanitized or '\\' in sanitized:
        raise ValueError("Nombre de archivo no válido")
    return sanitized

# Función para formatear nombres
def beautify_name(name):
    base_name, _ = os.path.splitext(name)
    formatted = re.sub(r'[-_]', ' ', base_name)
    return formatted.title()

# Ruta para el índice del catálogo
@app.route('/10/md_index')
def index():
    index_html = '<h2>Available Catalog:</h2><ul>'
    
    for root, _, files in os.walk(md_catalog):
        rel_path = os.path.relpath(root, md_catalog)
        rel_path = "" if rel_path == "." else rel_path
        
        if rel_path:
            folder_name = beautify_name(rel_path)
            index_html += f'<li><strong>{folder_name}</strong><ul>'
        
        for md_file in sorted(files):
            if md_file.endswith(('.md', '.markdown')):
                sanitized_name = sanitize_filename(md_file)
                display_name = beautify_name(md_file)
                file_name_without_ext = os.path.splitext(sanitized_name)[0]
                index_html += f'<li><a href="/10/md2web_tool/{file_name_without_ext}">{display_name}</a></li>'
        
        if rel_path:
            index_html += '</ul></li>'
    
    index_html += '</ul>'
    return Markup(index_html)

# Ruta para renderizar archivos Markdown
@app.route('/10/md2web_tool/<filename>')
def render_markdown(filename):
    sanitized_filename = sanitize_filename(filename)
    file_path = None

    for root, _, files in os.walk(md_catalog):
        for md_file in files:
            if sanitize_filename(md_file) == sanitized_filename and md_file.endswith(('.md', '.markdown')):
                file_path = os.path.join(root, md_file)
                break
        if file_path:
            break

    if not file_path:
        return render_template('404/index_404.html'), 404

    html_content = parser.parsing(file_path)
    if not html_content:
        return render_template('404/index_404.html'), 404

    page_title = os.path.splitext(filename)[0].replace('_', ' ')

    logging.debug(f"Ruta del archivo: {file_path}")
    logging.debug(f"Título de la página: {page_title}")
    logging.debug(f"Directorio del archivo: {os.path.dirname(file_path)}")

    return render_template('10/index_10.html', content=html_content, page_title=page_title, md_directory=os.path.dirname(file_path))

# Ruta para servir imágenes
@app.route('/10/md2web_tool/images/<path:filename>')
def serve_md_image(filename):
    md_directory = request.args.get('md_directory')
    if not md_directory:
        logging.error("Ruta no especificada para la imagen")
        return "Ruta no especificada", 404

    logging.debug(f"Sirviendo imagen: {filename} desde {md_directory}")  # Depuración
    return send_from_directory(md_directory, filename)

# Clase para procesar archivos Markdown
class ParsingMD:
    def parsing(self, file_path):
        if not os.path.exists(file_path):
            logging.error(f"Archivo no encontrado: {file_path}")
            return None
        
        try:
            with open(file_path, 'r', encoding='UTF-8') as f:
                md_content = f.read()
            logging.debug(f"Contenido Markdown leído: {md_content}")  # Depuración

            # Procesar el Markdown con las extensiones necesarias
            html_content = markdown.markdown(
                md_content, 
                extensions=['extra', 'tables', 'fenced_code', 'toc', 'md_in_html', 'attr_list', ImagePathExtension(file_path)]
            )
            logging.debug(f"Contenido HTML generado: {html_content}")  # Depuración
            return html_content
        except Exception as e:
            logging.error(f"Error al procesar el archivo {file_path}: {str(e)}")
            return None

# Clases para manejar rutas de imágenes en Markdown
class ImagePathExtension(Extension):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def extendMarkdown(self, md):
        md.inlinePatterns.register(ImagePathProcessor(r'!\[(.*?)\]\((.*?)\)', self.file_path), 'image_path', 175)

class ImagePathProcessor(ImageInlineProcessor):
    def __init__(self, pattern, file_path):
        super().__init__(pattern)
        self.file_path = file_path

    def handleMatch(self, m, data):
        # Llama al método handleMatch de la clase base para obtener el elemento HTML
        el, start, end = super().handleMatch(m, data)
        
        if el is not None:
            src = el.get('src')
            
            # Si la imagen tiene ruta relativa (no empieza con http:// o https://)
            if not src.startswith(('http://', 'https://')):
                # Limpiamos la ruta relativa (./ o ../)
                src = src.lstrip('./')

                # Construimos la nueva ruta para servir la imagen
                new_src = f"/10/md2web_tool/images/{src}?md_directory={os.path.dirname(self.file_path)}"
                logging.debug(f"Ruta de imagen modificada: {src} -> {new_src}")  # Depuración
                el.set('src', new_src)
                
        # Devuelve el elemento HTML y las posiciones de inicio y fin
        return el, start, end

# Instancia del parser
parser = ParsingMD()