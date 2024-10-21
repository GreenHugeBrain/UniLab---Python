from app import create_app, db
from flask_restful import Api
from resources import AddStudent, AddSubject, AddGrade, StudentById, SubjectById, GradeById

app = create_app()
api = Api(app)

api.add_resource(AddStudent, '/add_student')
api.add_resource(AddSubject, '/add_subject')
api.add_resource(AddGrade, '/add_grade')

api.add_resource(StudentById, '/student', '/student/<int:student_id>', '/student/name/<string:student_name>')
api.add_resource(SubjectById, '/subject', '/subject/<int:subject_id>', '/subject/name/<string:subject_name>')
api.add_resource(GradeById, '/grade', '/grade/<int:grade_id>', '/grade/student/<string:student_name>/subject/<string:subject_name>')

if __name__ == '__main__':
    app.run(debug=True)
