from wtforms import Form, StringField, DecimalField, validators


class ProductForm(Form):
    """
    WTForm for POST form data for new products
    - allows the inbuilt type validation to leveraged
    """
    name = StringField('name', validators=[validators.Length(min=1, max=64), validators.DataRequired()])
    price = DecimalField('price', validators=[validators.NumberRange(min=0.), validators.DataRequired()])
