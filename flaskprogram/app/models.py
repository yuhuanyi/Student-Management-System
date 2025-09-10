from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """用户模型，用于身份验证和权限管理"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)  # 唯一用户名，用于登录
    password = db.Column(db.Text, nullable=False)  # 加密后的密码

    def get_id(self):
        """返回用户ID作为字符串，满足Flask-Login要求"""
        return str(self.id)

    def __repr__(self):
        """对象的字符串表示，用于调试"""
        return f'<User {self.username}>'

class Student(db.Model):
    """学生基本信息模型"""
    __tablename__ = "student"
    student_id = db.Column(db.Text, primary_key=True)  # 学号作为主键
    name = db.Column(db.Text, nullable=False)  # 姓名
    gender = db.Column(db.Text, default="男")  # 性别，默认为男
    major = db.Column(db.Text, nullable=False)  # 专业
    class_ = db.Column("class", db.Text)  # 班级字段，使用"class"作为列名
    hometown = db.Column(db.Text)  # 籍贯
    password = db.Column(db.Text, nullable=False, default="123456")  # 默认密码

    def __repr__(self):
        """返回学生对象的标识信息"""
        return f'<Student {self.student_id}>'

class Course(db.Model):
    """课程信息模型"""
    __tablename__ = "course"
    course_id = db.Column(db.Integer, primary_key=True)  # 课程ID
    course_name = db.Column(db.Text, nullable=False)  # 课程名称
    credit = db.Column(db.Integer, nullable=False)  # 学分


    def __repr__(self):
        """返回课程对象的标识信息"""
        return f'<Course {self.course_name}>'

class Score(db.Model):
    """学生成绩关联模型，建立多对多关系"""
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True)  # 自增主键
    student_id = db.Column(db.Text, db.ForeignKey("student.student_id"), nullable=False)  # 关联学生
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)  # 关联课程
    score = db.Column(db.Float)  # 成绩分数

    # 定义关系映射
    student = db.relationship('Student', backref=db.backref('scores', lazy=True))  # 学生->成绩
    course = db.relationship('Course', backref=db.backref('scores', lazy=True))  # 课程->成绩

    def __repr__(self):
        """返回成绩记录的标识信息"""
        return f'<Score {self.student_id} {self.course_id}>'