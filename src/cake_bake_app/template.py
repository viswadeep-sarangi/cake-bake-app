from re import L
from typing import Dict
from fastapi.responses import HTMLResponse
import jinja2 as jj
from cake_bake_app import templates_dir
from datetime import datetime

report_template_fs = jj.Environment(loader=jj.FileSystemLoader(templates_dir))
test_template = report_template_fs.get_template("test.html")
add_employee_template = report_template_fs.get_template("add_employee.html")
submit_preference_template = report_template_fs.get_template("submit_preferences.html")
cake_resp_template = report_template_fs.get_template("cake_responsibility.html")
show_cake_resp_template = report_template_fs.get_template("show_cake_responsibility.html")

def generate_test_html_response():
    template_vars = {"timestamp":datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    html_content = test_template.render(template_vars)
    return HTMLResponse(content=html_content, status_code=200)

def generate_add_employee_template():
    return HTMLResponse(content=add_employee_template.render(), status_code=200)

def generate_submit_preference_template():
    return HTMLResponse(content=submit_preference_template.render(), status_code=200)

def generate_cake_responsibility_template():
    return HTMLResponse(content=cake_resp_template.render(), status_code=200)

def generate_show_cake_responsibility_template(vars:Dict[str,str]):
    html_content = show_cake_resp_template.render(vars)
    return HTMLResponse(content=html_content, status_code=200)