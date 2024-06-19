from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

username = 'postgres'
password = 'Kranthi'
host = '127.0.0.1'
port = '5432'
database = 'postgres'

engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, Sequence('student_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    major = Column(String(50))

    def __repr__(self):
        return f"<Student(id={self.id}, name={self.name}, age={self.age}, major={self.major})>"

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

@app.route('/')
def home():
    return "Welcome to the Student Management API"

@app.route('/students', methods=['POST'])
def create_student():
    new_student = request.get_json()
    student = Student(name=new_student['name'], age=new_student['age'], major=new_student['major'])
    session.add(student)
    session.commit()
    return jsonify(student.__dict__), 201
@app.route('/students', methods=['GET'])
def get_students():
    students = session.query(Student).all()
    stu_list = [{
        'id': student.id,
        'name': student.name,
        'age': student.age,
        'major': student.major
    } for student in students]
    return jsonify(stu_list), 200

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = session.query(Student).filter(Student.id == student_id).first()
    if student:
        return jsonify(student.__dict__)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = session.query(Student).filter(Student.id == student_id).first()
    if student:
        data = request.json
        student.name = data.get('name', student.name)
        student.age = data.get('age', student.age)
        student.major = data.get('major', student.major)
        session.commit()
        return jsonify(student.__dict__)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = session.query(Student).filter(Student.id == student_id).first()
    if student:
        session.delete(student)
        session.commit()
        return '', 204
    else:
        return jsonify({"error": "Student not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
