import random
from faker import Faker
from werkzeug.security import generate_password_hash
from app import db
from app.models import Student, Course, Score, User

fake = Faker("zh_CN")

'''
def generate_mock_data(student_count=100, course_count=8):
    """生成模拟数据"""
    # 清空现有数据
    db.session.query(Score).delete()
    db.session.query(Student).delete()
    db.session.query(Course).delete()
    db.session.query(User).delete()
    db.session.commit()

    # 创建课程
    courses = [
        ("高等数学", 5),
        ("线性代数", 4),
        ("Python程序设计", 3),
        ("数据结构", 4),
        ("数据库原理", 3),
        ("计算机网络", 4),
        ("机器学习", 3),
        ("Web开发", 3)
    ]

    course_objects = []
    for i, (name, credit) in enumerate(courses):
        course = Course(course_id=i + 1, course_name=name, credit=credit)
        course_objects.append(course)
        db.session.add(course)

    # 创建专业和生源地列表
    majors = [
        "数据科学",
        "计算机科学",
        "软件工程",
        "人工智能",
        "网络安全"
    ]
    hometowns = ["北京", "上海", "广州", "深圳", "杭州", "武汉", "成都", "重庆", "南京", "西安"]

    # 创建学生
    student_objects = []
    for i in range(student_count):
        student_id = f"230161{i + 1:04d}"
        student = Student(
            student_id=student_id,
            name=fake.name(),
            gender=random.choice(["男", "女"]),
            major=random.choice(majors),
            class_=f"{random.choice(majors)[0:2]}{random.randint(21, 23)}{i % 5 + 1:02d}",
            hometown=random.choice(hometowns),
            password="123456"
        )
        student_objects.append(student)
        db.session.add(student)

    # 为每个学生创建成绩
    for student in student_objects:
        # 随机选择5-8门课程
        selected_courses = random.sample(course_objects, k=random.randint(5, 8))
        for course in selected_courses:
            score = Score(
                student_id=student.student_id,
                course_id=course.course_id,
                score=round(random.uniform(50, 100), 1)
            )
            db.session.add(score)

    # 添加自定义学生
    my_student = Student(
        student_id="2301610230",
        name="虞桓毅",
        gender="男",
        major="数据科学与大数据技术",
        class_="23016102",
        hometown="黄石",
        password="123456"
    )
    db.session.add(my_student)

    # 为自定义学生添加所有课程成绩
    for course in course_objects:
        my_score = Score(
            student_id="2301610230",
            course_id=course.course_id,
            score=85.0
        )
        db.session.add(my_score)

    # 添加管理员用户 - 使用密码哈希
    admin_user = User(
        username="admin",
        password=generate_password_hash("admin123")
    )
    db.session.add(admin_user)

    # 添加测试用户
    test_user = User(
        username="test",
        password=generate_password_hash("test123")
    )
    db.session.add(test_user)

    db.session.commit()
    print(f"模拟数据生成完成：学生{student_count + 1}名，课程{course_count}门")
'''
