from flask import *

def renderContent(filepath, **kwargs):
    return render_template('index.html', content=Markup(render_template(filepath, **kwargs)))