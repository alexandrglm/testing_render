from flask import Blueprint, render_template

project11 = Blueprint('project11', __name__)

scenes = [
    {'title': '01 - Plane Shader Render', 'desc': 'Dynamic shader rendering for primitive planes, projected into a framebuffer which recreates directional movement with mouse/pointer. Library used:   THREE.js'},
    {'title': '02 - Spherical Scene 1: ', 'desc': ' Spherical VR scene with a fixed position. Libraries used: A-Frame / THREE.js'},
    {'title': '03 - Spherical Scene 2: ', 'desc': ' Spherical VR scene with custom shaders and grabable primitive polygons. Libraries used: A-Frame / THREE.js'},
    {'title': '04 - A-Frame Environment framework test 1 ', 'desc': ' Libraries used: A-Frame /  A-Frame-Environment-Component'},
    {'title': '05 - A-Frame Environment framework test 2', 'desc': ' Libraries used: A-Frame / A-Frame-Environment-Component'}
]

@project11.route('/')
def index_projects11():
    print("Scenes:", scenes)
    return render_template('11/index_11.html', scenes=scenes)


@project11.route('/<scene_id>/')
def render_scene(scene_id):
    scene_number = int(scene_id)

    if 1 <= scene_number <= len(scenes):

        template_path = f"11/11_{scene_id.zfill(2)}.html"

        return render_template(template_path, scene=scenes[scene_number - 1])
    
    else:

        return render_template('404/index_404.html'), 404
