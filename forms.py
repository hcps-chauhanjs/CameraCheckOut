from flask_wtf import FlaskForm
from wtforms import IntegerField, DateTimeField, FieldList, FormField
from wtforms.validators import InputRequired
from datetime import datetime
# my lord and savior: https://www.youtube.com/watch?v=K2czdygI2wM

class Equipment(FlaskForm):
    equipmentId = IntegerField('Equipment ID', validators=[InputRequired()])

class CourseForm(FlaskForm):
    studentId = IntegerField('Student ID', validators=[InputRequired()])
    equipments = FieldList(FormField(Equipment), min_entries=5, validators=[InputRequired()])
    
    # dateTime = DateTimeField('Date and Time', default=datetime.now, format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
