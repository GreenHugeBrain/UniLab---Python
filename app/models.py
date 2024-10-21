from app import db

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)

    grades = db.relationship('Grade', backref='student', lazy=True, cascade="all, delete-orphan") 

    def __repr__(self):
        return f"<Student {self.name} {self.lastname}>"

class Subject(db.Model):
    __tablename__ = 'subjects' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    grades = db.relationship('Grade', backref='subject', lazy=True)

    def __repr__(self):
        return f"<Subject {self.name}>"

class Grade(db.Model):
    __tablename__ = 'grades' 
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    grade_value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Grade {self.grade_value} for {self.subject.name} by {self.student.name}>"
