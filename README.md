export FLASK_APP=run.py
export FLASK_DEBUG=1

# 喵内

此项目是使用 Flask 构建的 RESTful api 应用。<br/>
在读完《流畅的 Python》之后想要做点什么东西，所以就有了这个项目<br/>

本项目有配套的 [前端项目](https://github.com/ShroXd/bebop-web)

## 运行

``` bash
# install dependencies
pip install -r requirements.txt

# configuration
export FLASK_APP=run.py
export FLASK_DEBUG=1

# run app
flask run
```

## 已完成
- 注册 / 登录
- 获取小说
- 获取章节
- 阅读
- 收藏
- 记录阅读进度
- Jenkins 自动化构建支持

## TODO
- 完成重构
- 拆分工具函数
