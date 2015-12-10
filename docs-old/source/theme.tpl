<div class="{{class|default('theme')}}">
<h2>{{name}}</h2>
{% if image %}
    <a href="/uploads/themes/{{image}}" class="thumbnail" target="_blank">
        <img src="/uploads/themes/{{image}}" class="img-responsive" />
    </a>
{% endif %}
<p>{{description}}</p>
{% if features %}
<h3>Features</h3>
<ul>
{% for f in features %}
    <li>{{f}}</li>
{% endfor %}
</ul>
{% endif %}
</div>
