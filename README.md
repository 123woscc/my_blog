# Flask博客1.0
## Introduction
个人博客项目初始版
使用技术: 
* 前端: Boostrap
* 后端: Flask

## Usage
1. 安装
```
pip install pipenv
pipenv install
```

2. 初始化
```
pipenv shell
python manage.py create_db
# 生成测试数据
python manage.py create_test_data
```

3. 运行
```
pipenv shell
python manage.py server
```
打开浏览器: http://localhost:5000

4. 配置
默认管理员账号:
```
username: admin
email: admin@cc.com
password: admin
```
## Bug
flask-admin部署报错 too many values to unpack (expected 2)
处理方法:
执行以下命令找到虚拟环境文件夹;
```
pipenv --venv
```
修改flask_admin/contrib/sqla/fields.py文件
```python
# flask_admin/contrib/sqla/fields.py
def get_pk_from_identity(obj):
    # TODO: Remove me
    print(obj.__dict__)
    print(obj.__dict__['id'])
    #cls, key = identity_key(instance=obj)
    key = identity_key(instance=obj)[1]
    return u':'.join(text_type(x) for x in key)
```
原理: app.cloudcone.com/compute

## API使用
1. 获取单篇文章:
格式:
[GET]http://127.0.0.1:5000/api/post?post_id=[文章id]
示例:
http://127.0.0.1:5000/api/post?post_id=1
2. 获取多篇文章:
格式:
[GET]http://127.0.0.1:5000/api/posts?page=[页数]&topic_id=[话题id]
示例:
    > 默认最新的10篇文章

    http://127.0.0.1:5000/api/posts
    > 获取的二页的10篇文章 

    http://127.0.0.1:5000/api/posts?page=2
    > 获取指定话题下的文章

    http://127.0.0.1:5000/api/posts?topic_id=2

3. 创建文章流程[基于HTTPBasicAuth]:
    * 授权获取token
    [GET]http://127.0.0.1:5000/api/token
    必选参数:
    email, password
    * 携带token创建文章
    [POST]http://127.0.0.1:5000/api/posts
    参数:
        title
        topic
        content

4. 获取文章的评论:
格式:
[GET] http://127.0.0.1:5000/api/comments?post_id=[文章id]
示例:
http://127.0.0.1:5000/api/comments?post_id=1
