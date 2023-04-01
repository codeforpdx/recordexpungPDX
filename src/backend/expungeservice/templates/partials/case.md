{% if case_info %}
       - {{ case_info }}
  {% for id, description in charges_info %}
           - {{ description }}
  {% endfor %}
{% else %}
  {% for id, description in charges_info %}
       - {{ description }}
  {% endfor %}
{% endif %}
