<div class="thumbnail" style="width: {{width|default('100%')}}; height: {{height|default('auto')}};">
    {% if url.startswith('/') or '://' in url %}
        {% set src = url %}
    {% else %}
        {% set src = conf.upload_web_path + '/' + url %}
    {% endif %}
    {% if nolink %}
    <img src="{{src}}" alt="{{alt|default('Image')}}" style="height: auto; width: 100%;" />
    {% else %}
    <a href="{{src}}" target="{{target|default('_blank')}}">
    <img src="{{src}}" alt="{{alt|default('Image')}}" style="height: auto; width: 100%;" />
    </a>
    {% endif %}
</div>
