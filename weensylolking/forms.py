from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class InputForm(Form):
    openid = StringField('openid', validators=[DataRequired()])

