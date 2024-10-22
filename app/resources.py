from flask_restful import Resource, Api, reqparse
from app import db
from models import Student, Subject, Grade

# Initialize request parsers
student_parser = reqparse.RequestParser()
subject_parser = reqparse.RequestParser()
grade_parser = reqparse.RequestParser()

# Define arguments for each parser
student_parser.add_argument('name', type=str, required=True)
student_parser.add_argument('lastname', type=str, required=True)

subject_parser.add_argument('name', type=str, required=True)

grade_parser.add_argument('student_id', type=int, required=True)
grade_parser.add_argument('subject_id', type=int, required=True)
grade_parser.add_argument('date', type=str, required=True)
grade_parser.add_argument('grade_value', type=float, required=True)

# Resource to add a student
class AddStudent(Resource):
    def post(self):
        args = student_parser.parse_args()
        new_student = Student(name=args['name'], lastname=args['lastname'])
        db.session.add(new_student)
        db.session.commit()
        return {'message': 'Student added successfully'}, 201

# Resource for retrieving, updating, and deleting students
class StudentById(Resource):
    def get(self, student_id=None, student_name=None):
        if student_id:
            student = Student.query.get(student_id)
            if student:
                grades = [{
                    'subject': grade.subject.name,
                    'grade_value': grade.grade_value,
                    'date': grade.date
                } for grade in student.grades]

                return {
                    'id': student.id,
                    'name': student.name,
                    'lastname': student.lastname,
                    'grades': grades  
                }, 200

        if student_name:
            students = Student.query.filter(Student.name.ilike(f'%{student_name}%')).all()
            if students:
                result = []
                for student in students:
                    grades = [{
                        'subject': grade.subject.name,
                        'grade_value': grade.grade_value,
                        'date': grade.date
                    } for grade in student.grades]

                    result.append({
                        'id': student.id,
                        'name': student.name,
                        'lastname': student.lastname,
                        'grades': grades
                    })

                return result, 200

            return {'message': 'No students found with that name'}, 404
        
        # Return all students if no filters are applied
        students = Student.query.all()
        result = []
        for student in students:
            grades = [{
                'subject': grade.subject.name,
                'grade_value': grade.grade_value,
                'date': grade.date
            } for grade in student.grades]

            result.append({
                'id': student.id,
                'name': student.name,
                'lastname': student.lastname,
                'grades': grades
            })

        return result, 200

    def delete(self, student_id):
        student = Student.query.get(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return {'message': 'Student deleted successfully'}, 200
        return {'message': 'Student not found'}, 404

# Resource to add a subject
class AddSubject(Resource):
    def post(self):
        args = subject_parser.parse_args()
        new_subject = Subject(name=args['name'])
        db.session.add(new_subject)
        db.session.commit()
        return {'message': 'Subject added successfully'}, 201

# Resource for retrieving, updating, and deleting subjects
class SubjectById(Resource):
    def get(self, subject_id=None, subject_name=None):
        if subject_id:
            subject = Subject.query.get(subject_id)
            if subject:
                return {'id': subject.id, 'name': subject.name}, 200
        
        if subject_name:
            subjects = Subject.query.filter(Subject.name.ilike(f'%{subject_name}%')).all()
            if subjects:
                return [{'id': subject.id, 'name': subject.name} for subject in subjects], 200
            return {'message': 'No subjects found with that name'}, 404
        
        # Return all subjects if no filters are applied
        subjects = Subject.query.all()
        result = []
        for subject in subjects:
            grades = [{
                'student': f"{grade.student.name} {grade.student.lastname}",
                'grade_value': grade.grade_value,
                'date': grade.date
            } for grade in subject.grades]

            result.append({
                'id': subject.id,
                'name': subject.name,
                'grades': grades
            })

        return result, 200

    def put(self, subject_id):
        subject = Subject.query.get(subject_id)
        if subject:
            args = subject_parser.parse_args()
            subject.name = args['name']
            db.session.commit()
            return {'message': 'Subject updated successfully'}, 200
        return {'message': 'Subject not found'}, 404

    def delete(self, subject_id):
        subject = Subject.query.get(subject_id)
        if subject:
            db.session.delete(subject)
            db.session.commit()
            return {'message': 'Subject deleted successfully'}, 200
        return {'message': 'Subject not found'}, 404

# Resource to add a grade
class AddGrade(Resource):
    def post(self):
        args = grade_parser.parse_args()
        student = Student.query.get(args['student_id'])
        subject = Subject.query.get(args['subject_id'])

        if not student:
            return {'message': 'Student not found'}, 404
        if not subject:
            return {'message': 'Subject not found'}, 404

        new_grade = Grade(
            student_id=args['student_id'],
            subject_id=args['subject_id'],
            date=args['date'],
            grade_value=args['grade_value']
        )
        db.session.add(new_grade)
        db.session.commit()
        return {'message': 'Grade added successfully'}, 201

# Resource for retrieving, updating, and deleting grades
class GradeById(Resource):
    def get(self, grade_id=None, student_name=None, subject_name=None):
        if grade_id:
            grade = Grade.query.get(grade_id)
            if grade:
                return {
                    'student_id': grade.student_id,
                    'subject_id': grade.subject_id,
                    'date': grade.date,
                    'grade_value': grade.grade_value
                }, 200

        if student_name and subject_name:
            student = Student.query.filter(Student.name.ilike(f'%{student_name}%')).first()
            subject = Subject.query.filter(Subject.name.ilike(f'%{subject_name}%')).first()
            
            if student and subject:
                grade = Grade.query.filter_by(student_id=student.id, subject_id=subject.id).first()
                if grade:
                    return {
                        'student_id': grade.student_id,
                        'subject_id': grade.subject_id,
                        'date': grade.date,
                        'grade_value': grade.grade_value
                    }, 200
                return {'message': 'Grade not found for given student and subject'}, 404
            return {'message': 'Student or Subject not found'}, 404
        
        # Return all grades if no filters are applied
        grades = Grade.query.all()
        result = [{
            'student_id': grade.student_id,
            'subject_id': grade.subject_id,
            'date': grade.date,
            'grade_value': grade.grade_value
        } for grade in grades]
        return result, 200

    def put(self, grade_id):
        grade = Grade.query.get(grade_id)
        if grade:
            args = grade_parser.parse_args()
            grade.student_id = args['student_id']
            grade.subject_id = args['subject_id']
            grade.date = args['date']
            grade.grade_value = args['grade_value']
            db.session.commit()
            return {'message': 'Grade updated successfully'}, 200
        return {'message': 'Grade not found'}, 404

    def delete(self, grade_id):
        grade = Grade.query.get(grade_id)
        if grade:
            db.session.delete(grade)
            db.session.commit()
            return {'message': 'Grade deleted successfully'}, 200
        return {'message': 'Grade not found'}, 404
