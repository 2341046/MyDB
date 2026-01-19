import os
from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

# .env ファイルから環境変数を読み込む（ローカル環境用）
load_dotenv()

app = Flask(__name__)

# --------------------------------------------------
# データベース設定
# --------------------------------------------------
db_user = os.getenv("DB_USERNAME")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --------------------------------------------------
# モデル定義
# --------------------------------------------------
class User(db.Model):
    """users テーブル（JSON取得用）"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)


class Category(db.Model):
    """TODOのカテゴリ"""
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    tasks = db.relationship(
        "Task",
        backref="category",
        cascade="all, delete-orphan",
        lazy=True
    )


class Task(db.Model):
    """TODOタスク"""
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

# --------------------------------------------------
# ルーティング
# --------------------------------------------------
@app.route("/")
def index():
    """users テーブルの内容を JSON 形式で返す"""
    users = User.query.order_by(User.id.asc()).all()
    return jsonify([
        {"id": u.id, "username": u.username}
        for u in users
    ])


@app.route("/todo")
def todo():
    """TODO画面を表示"""
    categories = Category.query.order_by(Category.id.asc()).all()
    cat_msg = request.args.get("cat_msg", "")
    task_msg = request.args.get("task_msg", "")
    return render_template(
        "todo.html",
        categories=categories,
        cat_msg=cat_msg,
        task_msg=task_msg
    )


@app.post("/categories/add")
def add_category():
    """カテゴリを追加"""
    name = (request.form.get("name") or "").strip()

    if not name:
        return redirect(url_for("todo", cat_msg="カテゴリ名が空です"))
    if Category.query.filter_by(name=name).first():
        return redirect(url_for("todo", cat_msg="そのカテゴリ名は既に存在しています"))

    db.session.add(Category(name=name))
    db.session.commit()
    return redirect(url_for("todo"))


@app.post("/categories/<int:category_id>/delete")
def delete_category(category_id: int):
    """カテゴリを削除（関連するタスクも削除）"""
    c = Category.query.get_or_404(category_id)
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for("todo"))


@app.post("/tasks/add")
def add_task():
    """タスクを追加"""
    title = (request.form.get("title") or "").strip()
    category_id = request.form.get("category_id")

    if not title:
        return redirect(url_for("todo", task_msg="タスク名が空です"))
    if not category_id:
        return redirect(url_for("todo", task_msg="カテゴリが選択されていません"))

    db.session.add(
        Task(
            title=title,
            category_id=int(category_id),
            done=False
        )
    )
    db.session.commit()
    return redirect(url_for("todo"))


@app.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id: int):
    """タスクの完了・未完了を切り替える"""
    t = Task.query.get_or_404(task_id)
    t.done = not t.done
    db.session.commit()
    return redirect(url_for("todo"))


@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id: int):
    """タスクを削除"""
    t = Task.query.get_or_404(task_id)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for("todo"))


@app.route("/health")
def health():
    """アプリケーションのヘルスチェック"""
    try:
        db.session.execute(db.text("SELECT 1"))
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify(
            {"status": "ng", "error": str(e)},
            500
        )
