from core.models import Student, Teacher

# Get teachers
ram = Teacher.objects.get(user__username='ram_sharma')
prem = Teacher.objects.get(user__username='prem_thapa')
shyam = Teacher.objects.get(user__username='shyam_shah')
gita = Teacher.objects.get(user__username='gita_tripathee')
guru = Teacher.objects.get(user__username='guru_nayak')

# School students (level=school, class 9-10)
s1 = Student.objects.create(name='Aryan Sharma', roll_number='S001', level='school', student_class='9', section='A')
s2 = Student.objects.create(name='Kiran Poudel', roll_number='S002', level='school', student_class='10', section='B')
# College students (level=college, XI-XII)
c1 = Student.objects.create(name='Manila Karki', roll_number='C001', level='college', student_class='XI', section='A')
c2 = Student.objects.create(name='Rijan Shrestha', roll_number='C002', level='college', student_class='XII', section='B')
# Bachelor students (level=bachelor, semesters)
b1 = Student.objects.create(name='Sita Gurung', roll_number='B001', level='bachelor', semester='1', section='A')
b2 = Student.objects.create(name='Rohit Adhikari', roll_number='B002', level='bachelor', semester='4', section='B')

# Assign all teachers to all students (subject-specific restriction enforced in views)
students = [s1, s2, c1, c2, b1, b2]
for stu in students:
    stu.teachers.add(ram, prem, shyam, gita, guru)

print('Students created and assigned successfully!')
print('Total students:', len(students))
