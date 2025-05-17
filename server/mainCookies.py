from server.mainObjects import projects,allowed_root_files,static_pages
import os
import importlib
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_socketio import SocketIO
from markupsafe import Markup


def route_Cookies(app):

    @app.context_processor
    def cookies_notice():

        def render_footer():
            return Markup(render_template('_footer.html'))

        return dict(render_footer = render_footer)
