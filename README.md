# 欢迎使用黄生生的博客

本博客基于Django2.0进行开发

## 使用前配置

1. 修改 `myblog/settings.py` 中相关配置
2. 安装相关包

    `pip install -r requirements.txt`
3. 安装mysql,并创建mysql_db数据库

    `create database myblog_db default charset=utf8mb4 default collate utf8mb4_unicode_ci;`
4. 初始化数据库

    `python manage.py migrate`
5. 创建缓存表

    `python manage.py createcachetable`
6. 安装mysql时区插件
    <https://dev.mysql.com/doc/refman/8.0/en/time-zone-support.html>
