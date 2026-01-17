# Docker-based TODO Application

## 概要
本プロジェクトは、データベース最終課題として作成した  
カテゴリ付き TODO アプリケーションです。

Docker Compose を用いて、  
Web / Application / Database の 3層構成を構築しています。

---

## システム構成

- Web：Nginx  
- Application：Flask + Gunicorn  
- Database：PostgreSQL  

---

## 使用技術

- Docker / Docker Compose  
- Nginx  
- Python 3.11  
- Flask / Flask-SQLAlchemy  
- PostgreSQL  

---

## ディレクトリ構成
my-todo-app/
├─ docker-compose.yml
├─ .gitignore
├─ app/
│ ├─ Dockerfile
│ ├─ requirements.txt
│ ├─ app.py
│ └─ templates/
│ ├─ index.html
│ └─ todo.html
├─ db/
│ └─ init.sql
└─ nginx/
└─ nginx.conf

※ `.env` は接続情報を含むため GitHub には含めていません。

---

## データベース

`db/init.sql` にて以下を実行しています。

- users / categories / tasks テーブル作成  
- 初期データ投入（users）

---

## 環境変数（.env）

プロジェクト直下に `.env` を作成してください。

```env
DB_USERNAME=guest
DB_PASSWORD=password
DB_HOST=db
DB_NAME=dbname

---

## 起動方法
docker compose up -d --build

---

## アクセス先

TODO アプリ画面
http://127.0.0.1:8080/todo

users 一覧（JSON）
http://127.0.0.1:8080/

---

## 役割分担

Infra：Docker / Nginx / Docker Compose

DBA：PostgreSQL / init.sql

Application：Flask / SQLAlchemy
