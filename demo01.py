
from flask import Flask,jsonify,session
from flask_sqlalchemy import SQLAlchemy
# 导包
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_script import Shell,Manager

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:mysql@127.0.0.1:3306/1903A'
app.config['SQLALCHEMY_TRACK_MODIFCATIONS']=True

db=SQLAlchemy(app)
# 实例化 脚本队象
migrate = Manager(app,db)
manger=Manager(app)

# 向控制台添加一个命令
manger.add_command('db',MigrateCommand)

# 作者表：
class Auth(db.Model):
    __tablename__='auth'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    gender=db.Column(db.String(8),default='女')
    age=db.Column(db.Integer,nullable=False,default=18)
    # 关系 联系，桥梁 依赖的是外键
    books=db.relationship('Books',backref='auth',lazy='dynamic')

    def todict(self):
        return {
            'id':self.id,
            'name':self.name
        }
# 图书表
class Books(db.Model):
    __tablename__='books'
    id=db.Column(db.Integer,primary_key=True)
    nmae=db.Column(db.String(100),nullable=False)
    price=db.Column(db.DECIMAL(8,2),default=999999.99)
    auth_id=db.Column(db.Integer,db.ForeignKey('auth.id'))

@app.route('/addauth/<name>')
def addauth(name):
    a=Auth()
    a.name=name
    # 写入数据
    db.session.add(a)
    db.session.commit()
    return '添加成功'

@app.route('/addboks/<authname>/<bookname>/<bookprice>')
def addboks(authname,bookname,bookprice):
#    查询作者
    a=Auth.query.filter(Auth.name==authname).first()

    # 实例化数据
    b=Books()
    b.nmae=bookname
    b.price=bookprice
    # b.auth_id=a.id

  # 添加书籍到数据库
  #   db.session.add(b)
    a.books.append(b)
    db.session.commit()
    # 第二种方式

# 通过关系 桥梁 reationship 来操作一对多关系

    return '添加成功'
@app.route('/searchbooks/<authname>')
def searchbooks(authname):
    a = Auth.query.filter(Auth.name==authname).first()
    if not a:
        return '请正确输入'
    for i in a.books:
        print(i.nmae)
    return 'ok'

@app.route('/searchauth/<bookname>')
def searchauth(bookname):
    #关系 联系 桥梁 依赖的外键。
    #books=db.relationship('Books',backref='auth',lazy='dynamic')
    b=Books.query.filter(Books.nmae == bookname).first()
    if not b:
        return '没找到'
    print(b.auth.name)
    return b.auth.name


@app.route('/all')
def all():
    a_list=Auth.query.all()
    list=[]
    # 将数据库的 行 转换为 列表 套字典
    for i in a_list:
        list.append(i.todict())

    return jsonify(a_list)
@app.route('/search/<name>')
def search(name):
    a=Auth.query.filter(Auth.name == name).first()
    return jsonify(a.todict())

@app.route('/change/<oldname>/<newname>')
def change(oldname,newname):

    #    查询
    a=Auth.query.filter(Auth.name==oldname).first()
    # 提交
    db.session.commit()
    return '修改成功{}》{}'.format(oldname,newname)


@app.route('/delete/<name>')
def delete(name):

    a=Auth.query.filter(Auth.name==name).first()
    # #    删除
    # db.session.delete(a)
    # db.session.commit()
    return '删除成功'



if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    # app.run()
    manger.run()

