from django.shortcuts import render
from matplotlib.pyplot import title
from database import db, app, User, Movie
from flask import render_template, request



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        try:
            userdata = User(email=email, username=username, password=password)
            db.session.add(userdata)
            db.session.commit()
        except Exception as e:
            print("error ", e)
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return render_template('home.html')
        else:
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/adminlogin', methods=['GET','POST'])
def adminlogin():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        return render_template('movie_add.html')
    return render_template('adminlogin.html')


@app.route('/movieadd', methods=['GET','POST'])
def movieadd():
    if request.method=='POST':
        title = request.form['title']
        director = request.form['director']
        actor1 = request.form['actor1']
        actor2 = request.form['actor2']
        actor3 = request.form['actor3']
        duration = request.form['duration']
        genre = request.form['genre']
        language = request.form['language']
        country = request.form['country']
        movie = Movie(title=title, actor1=actor1, actor2=actor2, actor3=actor3, director=director, genre=genre, language=language, country=country, TimeDuraton=duration)
        db.session.add(movie)
        db.session.commit()
        return render_template('movie_add.html')
    return render_template('movie_add.html')

@app.route('/home2')
def home2():
    return render_template('home 2.html')


@app.route('/moviebook',methods=['GET','POST'] )
def movieselect():
    movie = Movie.query.limit(9)
    titles = []
    for m in movie:
        titles.append(m.title)
    print(titles)
    return render_template('movie.html',titles = titles)


@app.route('/theatres', methods=['GET','POST'])
def theatres():
    if request.method=='POST':
        Time = request.form['options']
        print(Time)
        return render_template('book.html')
        

    return render_template('theatres.html')


@app.route('/book', methods=['GET','POST'])
def book():
    return render_template('book.html')


@app.route('/final', methods=['GET','POST'])
def final():
    l  = []
    if request.method=='POST':

        l = request.form.getlist('options')


    return render_template('final.html', length = len(l))

if __name__ == "__main__":
    
    app.run(debug=True)