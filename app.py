from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

# Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, default=0)

    def to_dict(self):
        return {
            'student_id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dob': self.dob.strftime('%Y-%m-%d'),
            'amount_due': self.amount_due
        }

# Create the database and tables (you need to run this only once)
with app.app_context():
    db.create_all()

# Routes for CRUD operations
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student.to_dict())

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    try:
        new_student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            dob=datetime.strptime(data['dob'], '%Y-%m-%d'),
            amount_due=data.get('amount_due', 0)
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify(new_student.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    data = request.get_json()
    try:
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.dob = datetime.strptime(data['dob'], '%Y-%m-%d')
        student.amount_due = data.get('amount_due', 0)

        db.session.commit()
        return jsonify(student.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)