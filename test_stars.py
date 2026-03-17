import jinja2

template_str = """
{% set rounded_rating = product.rating | round | int %}
{% for i in range(5) %}
    {% if i < rounded_rating %}
        <i class="fas fa-star"></i>
    {% else %}
        <i class="far fa-star"></i>
    {% endif %}
{% endfor %}
"""
template = jinja2.Template(template_str)

class Product:
    def __init__(self, rating):
        self.rating = rating

print("Rating 4.5:")
print(template.render(product=Product(4.5)))
print("Rating 0.0:")
print(template.render(product=Product(0.0)))
print("Rating 5.0:")
print(template.render(product=Product(5.0)))
