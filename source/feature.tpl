<div class="{{class|default('feature')}}">
    <h2>{{name}}</h2>
    {% if screenshot %}
    <a href="{{screenshot}}" target="{{target|default('_blank')}}" class="thumbnail">
    <img src="{{screenshot}}" class="img-responsive" alt="{{alt|default('feature')}}" />
    </a>
    {% endif %}
    <p>{{description}}</p>
    {% if link %}
    <a href="{{link}}" class="btn btn-primary">{{link_label|default('Learn more &raquo;')}}</a>
    {% endif %}
</div>
