from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, FloatField
from wtforms.validators import InputRequired, Length


class UsernameForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=5, max=10)],
    )


class PostForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[InputRequired(), Length(min=10, max=100)],
    )
    content = TextAreaField(
        "Content",
        validators=[InputRequired(), Length(min=5, max=1000)],
    )


class TipForm(FlaskForm):
    sender = StringField(
        "Sender",
    )

    recipient = StringField(
        "Recipient",
    )

    amount = FloatField(
        "Amount",
        validators=[InputRequired()],
    )
