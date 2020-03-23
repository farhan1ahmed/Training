from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired



class CreateTaskForm(FlaskForm):
    Title = StringField('Title', validators=[DataRequired()])
    Description = TextAreaField('Description', validators=[DataRequired()])
    Title = StringField('Title', validators=[DataRequired()])
    DueDate = DateField('Due Date', format='%d-%m-%Y', validators=[DataRequired()])
    Create = SubmitField('Create')