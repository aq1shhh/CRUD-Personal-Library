from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import String,Integer,Float

class Base(DeclarativeBase):
    pass

db=SQLAlchemy(model_class=Base)




'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///book-library.db"
app.secret_key="sevrc4vciu4viuc"
db.init_app(app)

class library(db.Model):
    id:Mapped[int]=mapped_column(Integer,primary_key=True,nullable=False)
    title:Mapped[str]=mapped_column(String,unique=True,nullable=False)
    author:Mapped[str]=mapped_column(String,nullable=False)
    rating:Mapped[float]=mapped_column(Float)

with app.app_context():
    db.create_all()




all_books = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/add",methods=["GET","POST"])
def add():
    if request.method=="POST":
        with app.app_context():
            new_book=library(title=request.form["bookname"],
                             author=request.form["author"],
                             rating=request.form['rating'])
            db.session.add(new_book)
            db.session.commit()

        post=library.query.all()



        return render_template("books.html",books=post)
    return render_template('add.html')

@app.route('/books',methods=["GET","POST"])

def books():
    post=library.query.all()
    return render_template('books.html',books=post)



@app.route('/edit_rating/<int:index>',methods=["GET","POST"])
def edit_rating(index):
    post = library.query.all()
    if request.method=="POST":
        new_rating=request.form['edit_rating']



        book_to_update=db.session.execute(db.select(library).where(library.id==index)).scalar()
        if book_to_update:
            book_to_update.rating=float(new_rating)
            db.session.commit()
            flash("Rating edited succesfully")

        else:
            flash("UNSCUESSFUL TRY AGAIN")
        return redirect(url_for('books', books=post))

    return render_template("edit_rating.html",books=post)


@app.route('/books/<int:index>',methods=["GET","POST"])
def delete(index):
        to_delete = db.session.execute(db.select(library).where(library.id == index)).scalar()
        if to_delete:

            db.session.delete(to_delete)
            db.session.commit()
        else:
            flash("Error couldnt delete")

        return redirect(url_for('books'))

if __name__ == "__main__":
    app.run(debug=True)

