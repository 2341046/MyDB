# Docker-based TODO Application

## 概要
本プロジェクトは、データベース最終課題として作成した、カテゴリ管理機能付きの TODO アプリケーションです。
Docker Compose を用いて、 Web / Application / Database の 3層構成 を構築しています。

---

## システム構成


* **Web**: Nginx (リバースプロキシ)
* **Application**: Flask + Gunicorn
* **Database**: PostgreSQL

---

## 使用技術
* **Infrastructure**: Docker / Docker Compose, Nginx
* **Backend**: Python 3.11, Flask, Flask-SQLAlchemy
* **Database**: PostgreSQL

---

## ディレクトリ構成
```text
my-todo-app/
├─ docker-compose.yml
├─ .gitignore
├─ app/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  ├─ app.py
│  └─ templates/
│      ├─ index.html
│      └─ todo.html
├─ db/
│  └─ init.sql
└─ nginx/
    └─ nginx.conf
```

※ .env は GitHub には含めていません。

---

## アクセス先
* TODO アプリ画面: http://127.0.0.1:8080/todo

* users 一覧（JSON）: http://127.0.0.1:8080/

