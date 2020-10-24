<select id="year" name="year">
    <!-- <option value="2018" selected>2018</option> -->
  {% for y in range(2018, 1904, -1) %}
  {% set y_str = y|string %}
     <option value="{{y_str}}">{{y}}</option>
  {% endfor %}
</select>
<select id="month" name="month">
    <!-- <option value="1" selected>1</option> -->
  {% for m in range(1, 13) %}
  {% set m_str = m|string %}
     <option value="{{m_str}}">{{m}}</option>
  {% endfor %}
</select>
<select id="day" name="day">
    <!-- <option value="1" selected>1</option> -->
  <!-- {% for d in range(2, 32) %}
  {% set d_str = d|string %}
     <option value="{{d_str}}">{{d}}</option>
  {% endfor %} -->
  <!-- the number of days in "day" also dynamically updates in js/monthDayGenerator.js -->
</select>
