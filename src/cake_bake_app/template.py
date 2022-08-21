from fastapi.responses import HTMLResponse
import jinja2 as jj
from cake_bake_app import templates_dir
from datetime import datetime

report_template_fs = jj.Environment(loader=jj.FileSystemLoader(templates_dir))
test_template = report_template_fs.get_template("test.html")
preferences_template = report_template_fs.get_template("cake_preferences.html")

def generate_test_html_response():
    template_vars = {"timestamp":datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    html_content = test_template.render(template_vars)
    return HTMLResponse(content=html_content, status_code=200)
