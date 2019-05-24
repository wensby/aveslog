from flask import render_template, g

def render_page(page):
  return render_template(page, **g.render_context)
