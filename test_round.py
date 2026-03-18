import jinja2

template_str = """
0.0 -> {{ (0.0 + 0.5) | int }}
4.0 -> {{ (4.0 + 0.5) | int }}
4.4 -> {{ (4.4 + 0.5) | int }}
4.5 -> {{ (4.5 + 0.5) | int }}
4.6 -> {{ (4.6 + 0.5) | int }}
5.0 -> {{ (5.0 + 0.5) | int }}
"""
print(jinja2.Template(template_str).render())
