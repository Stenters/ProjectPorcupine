from flask import *

def renderContent(filepath, **kwargs):
    # bC = 'backgroundColor' in 
    return render_template('index.html', content=Markup(render_template(filepath, **kwargs)))