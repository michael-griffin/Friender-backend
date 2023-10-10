# UsingWTForms to validate JSON

```python
@app.post('/api/get-lucky-num')
def get_lucky_num():

    form = JSONValidateForm(form_data=request.json, meta={'csrf': False})

    if form.validate_on_submit():
        lucky_num_data = generate_lucky_nums_json(request.json['year'])

        return jsonify(lucky_num_data)

    return jsonify({"errors": form.errors}), 400
```
