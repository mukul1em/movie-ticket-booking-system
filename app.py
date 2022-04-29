
from database import db, app, User, Movie
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, LoginManager, current_user

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route('/message')
def message():
    return render_template('message.html')
@app.route('/', methods=['GET', 'POST']) 
def main_home():
    return render_template('main_home.html')

@app.route('/admin_home', methods=['GET', 'POST'])
def admin_home():
    return render_template('admin_home.html')


@app.route('/adminedit', methods=['GET', 'POST','DELETE'] )
def adminedit():
    flag = False
    flag2 = False
    if request.method=='POST':
        form_name = request.form['form']
        flag3 = False
        print(form_name)    
        if form_name == "form1":

            name = request.form['movie']
            movie = Movie.query.filter_by(title=name).first()
            if movie:
                flag = True
                title = movie.title
                
                director = movie.director
                actor1 = movie.actor1
                actor2 = movie.actor2
                actor3 = movie.actor3
                overview = movie.description
                duration = movie.TimeDuraton
                return render_template('admin_edit.html', flag = flag, title=title,director=director,actor1=actor1, actor2=actor2,actor3=actor3,
                                            overview=overview, duration=duration)
            else:
                flag2  = True
                message = "movie not exist"
                return render_template('admin_edit.html', message=message, flag2=flag2)

        if form_name == "form3":
            flag2 = True
            name = request.form['movie']
            movie = Movie.query.filter_by(title=name).first()
            db.session.delete(movie)
            db.session.commit()
            message = "movie deleted"
            return render_template('admin_edit.html', message=message, flag2=flag2, name=name)

        
        if form_name == "form4":
            flag3 = True
            name = request.form['movie']
            print(name)
            message = "movie edited"
            return render_template('admin_edit.html', message=message, flag3=flag3, name=name)
        
        if form_name == "form5":
            flag3 = True
            duration = request.form['duration']
            overview = request.form['overview']
            name = request.form['edit_movie']
            movie = Movie.query.filter_by(title=name).first()
            print("edit movie name", movie.TimeDuraton)

            if duration and overview:
                movie.TimeDuraton = int(duration)
                movie.description = overview
                db.session.commit()
                message = "movie edited"
                return render_template('admin_edit.html', message=message, flag3=flag3)


            elif duration:
                movie.TimeDuraton = int(duration)
                db.session.commit()
                message = "movie edited"
                return render_template('admin_edit.html', message=message, flag3=flag3)
            elif overview:
                movie.description = overview
                db.session.commit()
                message = "movie edited"
                return render_template('admin_edit.html', message=message, flag3=flag3)
        
    return render_template('admin_edit.html', flag = flag)







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
            login_user(user)
            return redirect(url_for("home"))    
        else:
            return render_template('login.html')
    
    return render_template('login.html')


@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    
    return render_template('home.html', username=current_user.username)

@app.route('/adminlogin', methods=['GET','POST'])
def adminlogin():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        return render_template('admin_home.html')
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
    if request.method=='POST':
        time = "6:50 PM"
        form_name = request.form['form']
        if form_name == 'form1':
            print(request.form['movie'])
            tag = request.form['movie']
            search = "%{}%".format(tag)
            movie = Movie.query.filter(Movie.month > 5).filter(Movie.month < 9).filter(Movie.year==2022).filter(Movie.title.like(search)).limit(4)
        elif form_name == 'form2':
            tag = request.form['genre']
            search = "%{}%".format(tag)
            print(tag)
            movie = Movie.query.filter(Movie.month > 5).filter(Movie.month < 9).filter(Movie.year==2022).filter(Movie.genre.like(search)).limit(4)
        elif form_name == "form3":
            print(request.form['select'])
            return render_template('theatres.html', time=time)
        elif form_name == "form4":
            print(request.form['select'])
            return render_template('theatres.html',time=time)
        elif form_name == "form5":
            print(request.form['select'])
            return render_template('theatres.html', time=time)
        


        titles = []
        duration = []
        releasedates = []
        actors1 = []
        actors2 = []
        actors3 = []
        directors = []
        overview = []
        genres = []
        for m in movie:
            titles.append(m.title)
            duration.append(m.TimeDuraton)
            releasedates.append("-".join([str(m.month), str(m.year)]))
            actors1.append(m.actor1)
            actors2.append(m.actor2)
            actors3.append(m.actor3)
            directors.append(m.director)
            overview.append(m.description)
            genres.append(m.genre)
        return render_template('movie.html',titles = titles,duration=duration,
                                releasedates=releasedates,actors1=actors1, 
                                    actors2=actors2, actors3=actors3,
                                    directors=directors, overview=overview,genres=genres)

        # if request.form['movie'] :
        #     tag = request.form['movie']
        #     print(tag)
        #     search = "%{}%".format(tag)
        #     movie = Movie.query.filter(Movie.month > 5).filter(Movie.month < 9).filter(Movie.year==2022).filter(Movie.title.like(search)).limit(4)
        # elif request.form['movie'] != '':
        #     tag = request.form['movie']
        #     search = "%{}%".format(tag)
        #     print(tag)
        #     movie = Movie.query.filter(Movie.month > 5).filter(Movie.month < 9).filter(Movie.year==2022).filter(Movie.genre.like(search)).limit(4)
        # else:
        #     movie = Movie.query.filter(Movie.month > 5).filter(Movie.month < 9).filter(Movie.year==2022).limit(4)
        # titles = []
        # duration = []
        # releasedates = []
        # actors1 = []
        # actors2 = []
        # actors3 = []
        # directors = []
        # overview = []
        # genres = []
        # for m in movie:
        #     titles.append(m.title)
        #     duration.append(m.TimeDuraton)
        #     releasedates.append("-".join([str(m.month), str(m.year)]))
        #     actors1.append(m.actor1)
        #     actors2.append(m.actor2)
        #     actors3.append(m.actor3)
        #     directors.append(m.director)
        #     overview.append(m.description)
        #     genres.append(m.genre)
        
        # return render_template('movie.html',titles = titles,duration=duration,
        #                     releasedates=releasedates,actors1=actors1, 
        #                         actors2=actors2, actors3=actors3,
        #                         directors=directors, overview=overview,genres=genres, r= len(titles))
  
    if request.method=="GET":
        movie = Movie.query.filter(Movie.month > 5).filter(Movie.month < 9).filter(Movie.year==2022).limit(4)
        titles = []
        duration = []
        releasedates = []
        actors1 = []
        actors2 = []
        actors3 = []
        directors = []
        overview = []
        genres = []
        for m in movie:
            titles.append(m.title)
            duration.append(m.TimeDuraton)
            releasedates.append("-".join([str(m.month), str(m.year)]))
            actors1.append(m.actor1)
            actors2.append(m.actor2)
            actors3.append(m.actor3)
            directors.append(m.director)
            overview.append(m.description)
            genres.append(m.genre)
        return render_template('movie.html',titles = titles,duration=duration,
                                releasedates=releasedates,actors1=actors1, 
                                    actors2=actors2, actors3=actors3,
                                    directors=directors, overview=overview,genres=genres)


@app.route('/theatres', methods=['GET','POST'])
def theatres():
    time = "6:50 PM"
    if request.method=='POST':
        theatre = request.form['theatrename']
        Time = request.form['options']
        print(Time, theatre)
        return render_template('book.html', time = time)
        

    return render_template('theatres.html', time=time)


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