from flask import *
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Student, Course, Score, User

bp = Blueprint('main', __name__)

# 用户注册功能：处理用户注册请求，包括表单验证、密码加密和用户创建
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # 如果用户已登录，直接重定向到首页
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # 处理POST请求（表单提交）
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # 验证表单数据有效性
        errors = []
        if not username:
            errors.append('用户名不能为空')
        if not password or len(password) < 6:
            errors.append('密码长度至少为6位')
        if password != confirm_password:
            errors.append('两次输入的密码不一致')

        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            errors.append('该用户名已被注册')

        # 如果有错误，显示错误信息并返回注册页面
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html',
                                   username=username)

        # 创建新用户（密码加密存储）
        new_user = User(
            username=username,
            password=generate_password_hash(password)  # 使用werkzeug的哈希函数加密密码
        )

        # 保存到数据库
        db.session.add(new_user)
        db.session.commit()

        # 提示注册成功并跳转到登录页
        flash('注册成功！请登录', 'success')
        return redirect(url_for('main.login'))

    # GET请求：显示注册表单
    return render_template('register.html')


# 用户登录功能：验证用户身份并创建登录会话
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # 处理POST请求（表单提交）
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 查询用户
        user = User.query.filter_by(username=username).first()

        # 验证用户存在且密码正确
        if user and check_password_hash(user.password, password):
            login_user(user)  # 登录用户（Flask-Login功能）
            flash('登录成功！', 'success')
            return redirect(url_for('main.home'))  # 登录后跳转到首页
        # 验证失败，显示错误信息
        flash('用户名或密码错误', 'danger')
    # GET请求：显示登录表单
    return render_template('login.html')


# 用户登出功能：销毁用户登录会话
@bp.route('/logout')
@login_required  # 要求用户已登录才能访问
def logout():
    logout_user()  # 登出用户（Flask-Login功能）
    flash('您已成功退出系统', 'info')
    return redirect(url_for('main.login'))  # 登出后跳转到登录页


# 系统首页功能：显示系统概览数据和统计信息
@bp.route('/')
@login_required
def home():
    # 统计系统数据（学生、课程、成绩记录数量）
    student_count = Student.query.count()
    course_count = Course.query.count()
    score_count = Score.query.count()

    # 获取最新添加的5名学生（按学号倒序排序）
    recent_students = Student.query.order_by(Student.student_id.desc()).limit(5).all()

    # 渲染首页模板并传递统计数据
    return render_template('home.html',
                           student_count=student_count,
                           course_count=course_count,
                           score_count=score_count,
                           recent_students=recent_students)


# 学生列表功能：展示所有学生信息，支持搜索和分页
@bp.route('/students')
@login_required
def student_list():
    # 获取搜索关键词和页码参数
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每页显示10条记录

    # 根据搜索关键词过滤学生（支持按姓名、学号、专业搜索）
    if search:
        students = Student.query.filter(
            (Student.name.contains(search)) |
            (Student.student_id.contains(search)) |
            (Student.major.contains(search))
        ).paginate(page=page, per_page=per_page)
    else:
        # 无搜索时查询所有学生并分页
        students = Student.query.paginate(page=page, per_page=per_page)

    # 渲染学生列表模板
    return render_template('student/list.html',
                           students=students,
                           search=search,
                           pagination=students)


# 添加学生功能：处理学生信息的添加
@bp.route('/students/add', methods=['GET', 'POST'])
@login_required
def student_add():
    # 处理POST请求（表单提交）
    if request.method == 'POST':
        # 获取表单数据
        student_id = request.form['student_id']
        name = request.form['name']
        gender = request.form['gender']
        major = request.form['major']
        class_ = request.form['class_']
        hometown = request.form['hometown']

        # 检查学号是否已存在
        if Student.query.filter_by(student_id=student_id).first():
            flash('该学号已存在', 'danger')
            return redirect(url_for('main.student_add'))

        # 创建学生对象
        student = Student(
            student_id=student_id,
            name=name,
            gender=gender,
            major=major,
            class_=class_,
            hometown=hometown
        )

        # 保存到数据库
        db.session.add(student)
        db.session.commit()
        flash('学生信息添加成功', 'success')
        return redirect(url_for('main.student_list'))  # 添加后跳转到学生列表

    # GET请求：显示添加学生表单
    return render_template('student/form.html')


# 编辑学生功能：处理学生信息的修改
@bp.route('/students/edit/<student_id>', methods=['GET', 'POST'])
@login_required
def student_edit(student_id):
    # 查询学生，不存在则返回404
    student = Student.query.get_or_404(student_id)

    # 处理POST请求（表单提交）
    if request.method == 'POST':
        # 更新学生信息
        student.name = request.form['name']
        student.gender = request.form['gender']
        student.major = request.form['major']
        student.class_ = request.form['class_']
        student.hometown = request.form['hometown']

        # 保存修改
        db.session.commit()
        flash('学生信息更新成功', 'success')
        return redirect(url_for('main.student_list'))  # 编辑后跳转到学生列表

    # GET请求：显示编辑表单（携带当前学生信息）
    return render_template('student/edit.html', student=student)


# 删除学生功能：删除指定学生及其关联的成绩记录
@bp.route('/students/delete/<student_id>', methods=['POST'])
@login_required
def student_delete(student_id):
    # 查询学生，不存在则返回404
    student = Student.query.get_or_404(student_id)
    # 先删除该学生的所有成绩记录（外键约束）
    Score.query.filter_by(student_id=student_id).delete()
    # 删除学生
    db.session.delete(student)
    db.session.commit()
    flash('学生信息已删除', 'success')
    return redirect(url_for('main.student_list'))  # 删除后跳转到学生列表


# 学生成绩详情功能：展示指定学生的所有成绩及统计信息
@bp.route('/student_scores/<int:student_id>')
def student_scores(student_id):
    # 查询学生，不存在则返回404
    student = Student.query.get_or_404(student_id)
    # 获取该学生的所有成绩
    scores = Score.query.filter_by(student_id=student_id).all()

    # 统计成绩分布区间（不及格、及格、优秀）
    score_distribution = {
        "不及格": 0,
        "及格": 0,
        "优秀": 0
    }
    for score in scores:
        if score.score < 60:
            score_distribution["不及格"] += 1
        elif 60 <= score.score < 90:
            score_distribution["及格"] += 1
        elif score.score >= 90:
            score_distribution["优秀"] += 1

    # 计算平均分
    total = sum(score.score for score in scores)
    average_score = total / len(scores) if scores else 0

    # 渲染成绩详情模板
    return render_template('student/scores.html',
                           student=student,
                           scores=scores,
                           average_score=average_score,
                           score_distribution=score_distribution)


# 课程列表功能：展示所有课程信息，支持搜索和分页
@bp.route('/courses')
@login_required
def course_list():
    # 获取搜索关键词和页码参数
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每页显示10条记录

    # 根据搜索关键词过滤课程（支持按课程ID、名称、学分搜索）
    if search:
        courses = Course.query.filter(
            (Course.course_id.contains(search)) |
            (Course.course_name.contains(search)) |
            (Course.credit.contains(search))
        ).paginate(page=page, per_page=per_page)
    else:
        # 无搜索时查询所有课程并分页
        courses = Course.query.paginate(page=page, per_page=per_page)

    # 渲染课程列表模板
    return render_template('course/list.html',
                           courses=courses,
                           search=search,
                           pagination=courses)


# 添加课程功能：处理课程信息的添加
@bp.route('/courses/add', methods=['GET', 'POST'])
@login_required
def course_add():
    # 处理POST请求（表单提交）
    if request.method == 'POST':
        course_name = request.form['course_name']
        credit = request.form['credit']

        # 检查课程是否已存在
        if Course.query.filter_by(course_name=course_name).first():
            flash('该课程已存在', 'danger')
            return redirect(url_for('main.course_add'))

        # 创建课程对象
        course = Course(course_name=course_name, credit=credit)
        # 保存到数据库
        db.session.add(course)
        db.session.commit()
        flash('课程信息添加成功', 'success')
        return redirect(url_for('main.course_list'))  # 添加后跳转到课程列表

    # GET请求：显示添加课程表单
    return render_template('course/form.html')


# 编辑课程功能：处理课程信息的修改
@bp.route('/courses/edit/<int:course_id>', methods=['GET', 'POST'])
@login_required
def course_edit(course_id):
    # 查询课程，不存在则返回404
    course = Course.query.get_or_404(course_id)

    # 处理POST请求（表单提交）
    if request.method == 'POST':
        # 更新课程信息
        course.course_name = request.form['course_name']
        course.credit = request.form['credit']
        # 保存修改
        db.session.commit()
        flash('课程信息更新成功', 'success')
        return redirect(url_for('main.course_list'))  # 编辑后跳转到课程列表

    # GET请求：显示编辑表单（携带当前课程信息）
    return render_template('course/edit.html', course=course)


# 删除课程功能：删除指定课程及其关联的成绩记录
@bp.route('/courses/delete/<int:course_id>', methods=['POST'])
@login_required
def course_delete(course_id):
    # 查询课程，不存在则返回404
    course = Course.query.get_or_404(course_id)
    # 先删除该课程的所有成绩记录（外键约束）
    Score.query.filter_by(course_id=course_id).delete()
    # 删除课程
    db.session.delete(course)
    db.session.commit()
    flash('课程信息已删除', 'success')
    return redirect(url_for('main.course_list'))  # 删除后跳转到课程列表


# 成绩录入功能：处理学生成绩的添加或更新
@bp.route('/scores/input', methods=['GET', 'POST'])
@login_required
def score_input():
    # 处理POST请求（表单提交）
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        score_value = request.form['score']

        # 验证学生是否存在
        if not Student.query.get(student_id):
            flash('学生不存在', 'danger')
            return redirect(url_for('main.score_input'))

        # 验证课程是否存在
        if not Course.query.get(course_id):
            flash('课程不存在', 'danger')
            return redirect(url_for('main.score_input'))

        # 检查该学生的该课程成绩是否已存在
        existing_score = Score.query.filter_by(
            student_id=student_id,
            course_id=course_id
        ).first()

        # 存在则更新，不存在则创建
        if existing_score:
            existing_score.score = score_value
            flash('成绩已更新', 'success')
        else:
            score = Score(
                student_id=student_id,
                course_id=course_id,
                score=score_value
            )
            db.session.add(score)
            flash('成绩录入成功', 'success')

        # 保存到数据库
        db.session.commit()
        return redirect(url_for('main.score_input'))  # 操作后仍停留在成绩录入页

    # GET请求：显示成绩录入表单
    return render_template('score/input.html')


# 成绩查询功能：根据学生或课程筛选成绩记录
@bp.route('/scores/query')
@login_required
def score_query():
    # 获取查询参数（学生ID和课程ID）
    student_id = request.args.get('student_id')
    course_id = request.args.get('course_id')

    # 构建查询（关联成绩、学生、课程表）
    query = db.session.query(Score, Student, Course). \
        join(Student, Score.student_id == Student.student_id). \
        join(Course, Score.course_id == Course.course_id)

    # 根据参数筛选
    if student_id:
        query = query.filter(Score.student_id == student_id)
    if course_id:
        query = query.filter(Score.course_id == course_id)

    # 执行查询
    results = query.all()

    # 整理数据用于模板显示
    scores = []
    for score, student, course in results:
        scores.append({
            'student_id': score.student_id,
            'student_name': student.name,
            'course_id': score.course_id,
            'course_name': course.course_name,
            'score': score.score
        })

    # 获取所有学生和课程用于查询表单的下拉菜单
    students = Student.query.all()
    courses = Course.query.all()

    # 渲染成绩查询结果模板
    return render_template('score/query.html',
                           scores=scores,
                           students=students,
                           courses=courses,
                           student_id=student_id or '',
                           course_id=course_id or '')


# 数据可视化功能：展示成绩分布、专业对比等统计图表数据
@bp.route('/visualization')
@login_required
def visualization():
    # 1. 整体成绩分布数据（按分数段统计）
    distribution = {
        '<60': 0,
        '60-70': 0,
        '70-80': 0,
        '80-90': 0,
        '90-100': 0
    }

    scores = Score.query.all()
    for score in scores:
        if score.score < 60:
            distribution['<60'] += 1
        elif score.score < 70:
            distribution['60-70'] += 1
        elif score.score < 80:
            distribution['70-80'] += 1
        elif score.score < 90:
            distribution['80-90'] += 1
        else:
            distribution['90-100'] += 1

    # 2. 专业平均分数据
    majors = [
        "数据科学",
        "计算机科学",
        "软件工程",
        "人工智能",
        "网络安全"
    ]

    major_scores = []
    for major in majors:
        # 查询该专业的所有学生
        students = Student.query.filter_by(major=major).all()
        student_ids = [s.student_id for s in students]

        # 计算该专业所有学生的平均成绩
        avg_score = db.session.query(
            db.func.avg(Score.score)
        ).filter(Score.student_id.in_(student_ids)).scalar()

        # 无成绩时默认70分
        major_scores.append(round(avg_score or 70, 1))

    # 3. 课程平均分及箱线图数据
    # 按课程ID排序查询所有课程
    courses = Course.query.order_by(Course.course_id).all()
    course_names = []  # 课程名称列表
    course_avgs = []   # 课程平均分列表
    boxplot_data = []  # 箱线图数据（用于展示成绩分布）

    # 按课程分类收集成绩
    course_scores = {}
    for course in courses:
        course_names.append(course.course_name)
        scores_for_course = [s.score for s in course.scores]
        course_scores[course.course_id] = scores_for_course

        # 计算课程平均分
        avg_score = db.session.query(
            db.func.avg(Score.score)
        ).filter_by(course_id=course.course_id).scalar()
        course_avgs.append(round(avg_score or 0, 1))

    # 计算箱线图所需的统计指标（最小值、下四分位数、中位数、上四分位数、最大值）
    for course_id in sorted(course_scores.keys()):
        scores_for_course = course_scores[course_id]

        if scores_for_course:
            min_val = max(min(scores_for_course), 50)  # 确保最低分不低于50
            max_val = max(scores_for_course)
            sorted_scores = sorted(scores_for_course)
            n = len(sorted_scores)

            # 计算中位数
            if n % 2 == 1:
                median = sorted_scores[n // 2]
            else:
                median = (sorted_scores[n // 2 - 1] + sorted_scores[n // 2]) / 2.0

            # 计算下四分位数 (Q1)
            q1_pos = n // 4
            q1 = sorted_scores[q1_pos] if n % 4 != 0 else (sorted_scores[q1_pos - 1] + sorted_scores[q1_pos]) / 2.0

            # 计算上四分位数 (Q3)
            q3_pos = 3 * n // 4
            q3 = sorted_scores[q3_pos] if n % 4 != 0 else (sorted_scores[q3_pos - 1] + sorted_scores[q3_pos]) / 2.0

            boxplot_data.append([min_val, q1, median, q3, max_val])
        else:
            # 无成绩时使用默认值
            boxplot_data.append([60, 68, 75, 82, 90])

    # 4. 生源地分布数据（统计各地区的学生数量）
    hometowns = db.session.query(
        Student.hometown,
        db.func.count(Student.student_id)
    ).group_by(Student.hometown).all()

    hometown_names = [h[0] for h in hometowns]  # 生源地名称
    hometown_counts = [h[1] for h in hometowns]  # 各生源地学生数量

    # 5. 各课程成绩分布数据
    course_distributions = {}
    for course in courses:
        course_dist = {
            '<60': 0,
            '60-70': 0,
            '70-80': 0,
            '80-90': 0,
            '90-100': 0
        }
        # 统计该课程各分数段的人数
        for score in course.scores:
            if score.score < 60:
                course_dist['<60'] += 1
            elif score.score < 70:
                course_dist['60-70'] += 1
            elif score.score < 80:
                course_dist['70-80'] += 1
            elif score.score < 90:
                course_dist['80-90'] += 1
            else:
                course_dist['90-100'] += 1
        course_distributions[course.course_id] = course_dist

    # 渲染可视化页面模板，传递所有统计数据
    return render_template('visualization/index.html',
                           distribution=distribution,
                           course_distributions=course_distributions,
                           major_scores=major_scores,
                           majors=majors,
                           course_names=course_names,
                           course_avgs=course_avgs,
                           boxplot_data=boxplot_data,
                           hometown_names=hometown_names,
                           hometown_counts=hometown_counts,
                           courses=courses)