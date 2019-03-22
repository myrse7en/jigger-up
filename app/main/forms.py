from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User
import os
import requests

class ProfileEditorForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    headline = TextAreaField('Headline', validators=[Length(min=0, max=140)])
    bio = TextAreaField('About Me', validators=[Length(min=0, max=500)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(ProfileEditorForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')


class RecipeSearch(FlaskForm):
    ingredient = StringField('Ingredient: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def getRecipeByIngredients(ingredients):
        return

    def getRecipeURL(id):
        return
