<div style="border: 1px solid #ddd; background: #eee;">
    <p>{{title}}</p>
    <p>Rating: 
    {% for i in range(rating) %}
        <b>X</b>
    {% endfor %}
    </p>
</div>
