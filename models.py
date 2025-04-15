#imports for the models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from algorithms import tdee

#initialize the database
db = SQLAlchemy()

#create the nutrition log model
class NutritionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)  # Ensure user_id is not null
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    activity_level = db.Column(db.String(20), nullable=True)
    fat_logs = db.Column(db.JSON, nullable=True)
    protein_logs = db.Column(db.JSON, nullable=True)
    carbs_logs = db.Column(db.JSON, nullable=True)
    cal_in_logs = db.Column(db.JSON, nullable=True)
    cal_out_logs = db.Column(db.JSON, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    #calculate the cal_out use tdee function
    @property
    def cal_out(self):
        if self.gender and self.age and self.weight and self.height and self.activity_level:
            return tdee(self.gender, self.age, self.weight, self.height, self.activity_level)
        return None
    
    #convert the model to a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'gender': self.gender,
            'age': self.age,
            'weight': self.weight,
            'height': self.height,
            'activity_level': self.activity_level,
            'fat_logs': self.fat_logs,
            'protein_logs': self.protein_logs,
            'carbs_logs': self.carbs_logs,
            'cal_in_logs': self.cal_in_logs,
            'cal_out_logs': self.cal_out_logs,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'email': self.email
        }