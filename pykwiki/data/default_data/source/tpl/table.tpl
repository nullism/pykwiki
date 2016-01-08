<table class="data-table">
{% if headers %}
    <thead>
    <tr>
    {% for head in headers %}
        <th>{{head}}</th>
    {% endfor %}
    </tr>
    </thead>
{% endif %}
<tbody>
{% for row in rows %}
    <tr>
    {% for col in row %}
        <td>{{col}}</td>
    {% endfor %}
    </tr>
{% endfor %}
</tbody>
</table>
