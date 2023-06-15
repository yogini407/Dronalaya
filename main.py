#from model import create_app
from flask import Flask,render_template,url_for,request,redirect,session
import mysql.connector
import os

import pickle
#jobs module
popular_df = pickle.load(open('popular.pkl','rb'))
jobs = pickle.load(open('jobs.pkl','rb'))
dom_similarity = pickle.load(open('dom_similarity.pkl','rb'))
loc_similarity = pickle.load(open('loc_similarity.pkl','rb'))
course_df = pickle.load(open('course_df.pkl','rb'))


app = Flask(__name__)
app.secret_key= os.urandom(24)

conn = mysql.connector.connect(host="127.0.0.1", user="root",password="sample123",database="dronalaya_login")
cursor = conn.cursor()

# if __name__ == '__main__':
#     app.run(debug=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('index.html')

@app.route('/features')
def features():
    return render_template('index.html')

@app.route('/trend_jobs')
def trend_jobs():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_validation', methods=['POST','GET'])
def login_validation():
    username = request.form.get('email')
    # uname = cursor.query['username']
    email = request.form.get('email')
    password = request.form.get('password')
    type = request.form.get('type')
    cursor.execute("""SELECT * FROM `userlogin` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
    users = cursor.fetchall()

    # cursor.execute("""SELECT * FROM `userlogin` WHERE `username` LIKE '{}' AND `type` LIKE '{}'""".format(uname))
    # user1= cursor.fetchall()

    if len(users)>0:
        session['user_id']=users[0][0]
        return render_template('profile.html',name=email)
    else:
        return redirect('/login')
    #print(users)

    # uname = request.form['username']
    # email = request.form['email']
    # password = request.form['password']
    # cursor.execute("""SELECT * FROM `userlogin` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password,uname))
    # users_data = cursor.fetchall()
    # if email not in users:
    #     return render_template('login.html', info='Invalid User')
    # else:
    #     if users[email] != password:
    #         return render_template('login.html', info='Invalid Password')
    #     else:
    #         return render_template('profile.html',name=email)
    #
    # #return "hello world"

@app.route('/register_user' , methods = ['POST'])
def register_user():
    username=request.form.get('username')
    email=request.form.get('useremail')
    password = request.form.get('userpassword')
    confirmpass = request.form.get('userpassword1')
    mobile= request.form.get('mobile')
    type=request.form.get('user_question')

    cursor.execute("""INSERT INTO `userlogin` (`user_id`,`username`,`email`,`password`,`confirmpass`,`mobile`,`type`) VALUES 
    (NULL, '{}','{}','{}','{}','{}','{}')""".format(username,email,password,confirmpass,mobile,type))
    conn.commit()

    cursor.execute("""SELECT * FROM `userslogin` WHERE `email` LIKE '{}'""".format(email))
    myuser = cursor.fetchall()
    session['user_id'] = myuser[0][0]
    return redirect('/profile')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        return render_template('profile.html')
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/jobspage')
def jobspage():
    return render_template('light_contact_list.html',
                    domain = list(popular_df['domain'].values),
                    jobtitle=list(popular_df['jobtitle'].values),
                    salary=list(popular_df['salary'].values),
                    jobtype=list(popular_df['jobtype'].values),
                    location=list(popular_df['location'].values),
                    url=list(popular_df['url'].values)
                    )

@app.route('/coursespage')
def coursespage():
    return render_template('courseRecommend.html',
                    domain = list(course_df['domain'].values),
                    course_title=list(course_df['course_title'].values),
                    enrolled=list(course_df['enrolled'].values),
                    url=list(course_df['url'].values)
                    )

@app.route('/recommend')
def recommend_ui():
    return render_template('profile.html')

# @app.route('/recommend_jobs', methods=['post'])
# def recommend(domain,loc):
#     job_index1 = jobs[jobs['domain'] == domain].index[0]
#     distances1 = dom_similarity[job_index1]
#     #     job_index2 = jobs[jobs['recenteducation']==edu].index[0]
#     #     distances2 = edu_similarity[job_index2]
#     #     job_index3 = jobs[jobs['skills']==skills].index[0]
#     #     distances3 = skills_similarity[job_index3]
#     # job_index4 = jobs[jobs['jobtype'] == jtype].index[0]
#     # distances4 = type_similarity[job_index4]
#     #     job_index5 = jobs[jobs['experience']==exp].index[0]
#     #     distances5 = exp_similarity[job_index5]
#     job_index6 = jobs[jobs['location'] == loc].index[0]
#     distances6 = loc_similarity[job_index6]
#     # job_index7 = jobs[jobs['salary'] == sal].index[0]
#     # distances7 = sal_similarity[job_index7]
#
#     jobs_list = sorted(list(enumerate(distances1)), reverse=True, key=lambda x: x[1])[1:10]
#     #     jobs_list = sorted(list(enumerate(distances2)),reverse =True, key= lambda x:x[1])[1:6]
#     #     jobs_list = sorted(list(enumerate(distances3)),reverse =True, key= lambda x:x[1])[1:6]
#     # jobs_list = sorted(list(enumerate(distances4)), reverse=True, key=lambda x: x[1])[1:10]
#     #     jobs_list = sorted(list(enumerate(distances5)),reverse =True, key= lambda x:x[1])[1:6]
#     jobs_list = sorted(list(enumerate(distances6)), reverse=True, key=lambda x: x[1])[1:10]
#     # jobs_list = sorted(list(enumerate(distances7)), reverse=True, key=lambda x: x[1])[1:10]
#
#     data = []
#     for i in jobs_list:
#         items = []
#         items.extend(list(jobs.iloc[i[0]].jobtitle)['domain'].values)
#         items.extend(list(jobs.iloc[i[0]].jobtitle)['jobtitle'].values)
#         items.extend(list(jobs.iloc[i[0]].jobtitle)['salary'].values)
#         items.extend(list(jobs.iloc[i[0]].jobtitle)['jobtype'].values)
#         items.extend(list(jobs.iloc[i[0]].jobtitle)['location'].values)
#         items.extend(list(jobs.iloc[i[0]].jobtitle)['url'].values)
#         data.append(items)
#     print(data)
#     # return 'Hello'

if __name__ == '__main__':
    app.run(debug=True)
    # recommend('frontend development','mumbai')
