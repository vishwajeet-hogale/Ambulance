from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import random
import matrix as m
import json
app=Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mysteriousman307'
app.config['MYSQL_DB'] = 'ambulance'
mysql = MySQL(app)

app.secret_key = "mysecretkey"
oadd = None
dadd = None
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/getdata',methods=['POST','GET'])
def formfill():
    if request.method == 'POST':
        global oadd
        global dadd
        patientName = request.form['name']
        patientAge = int(request.form['age'])
       
        flash('Thank you! Your ambulance will arrive soon')
        obname = request.form['bname']
        oaname = request.form['aname']
        oadd = obname + ',' + oaname
        dbname = request.form['hname']
        daname = request.form['haname']
        dadd = dbname + ',' + daname
        points = m.get_latlong(obname,oaname,dbname,daname)
        j = m.getpoints(points[0][0],points[0][1],points[1][0],points[1][1])
        origin=[points[0][0],points[0][1]]
        dest=[points[1][0],points[1][1]]
        print(j[0]['numofpoints'])
        lat = []
        lon=[]
        lat=j[0]['latpoints']
        lon=j[0]['longpoints']
        print(lat)
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM trafficsignals")
        data = cur.fetchall()
        cur.close()
        latsig = []
        longsig =[]
        for i in data:
            latsig.append(i[1])
            longsig.append(i[2])
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM congestion")
        avg_and_red = list(cur.fetchall())
        avg_times = [i[2] for i in avg_and_red]
        red_time = [i[3] for i in avg_and_red]
        print(avg_times)
        cur.close()
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM trafficsignals")
        dat = cur.fetchall()
        weight_baba = [i[3] for i in dat]

        
        return render_template('map.html',lat=lat,long=lon,origin=origin,dest=dest,latsig=latsig,longsig=longsig,avg_time=avg_times,red_time=red_time,weights=weight_baba)
      
@app.route('/ouranalysis')
def getanalysis():
    global oadd
    global dadd
    print(oadd)
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM trafficsignals")
    data = cur.fetchall()
    l=[]
    cur.close()
    

    for i in range(0,len(data)):
        b=m.get_reverse_geo(data[i][1],data[i][2])
        b = b.split(',')
        b = b[0:5]
        l.append(','.join(b))
    
    return render_template('analysis.html',signals = data,l=l,length=len(l),origin=oadd,dest=dadd)
        
if __name__ == '__main__':
    app.run(debug=True,port=5000)