from flask import Flask, jsonify
import mysql.connector
from datetime import datetime

#pip install mysql.connector
#pip install flask
#Enviroment ayarlamak için CMD komutları
# 'set FLASK_APP=hello'
# 'flask run'

#MySQL database için ayarlar.
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mechsoftt"
)
mycursor = mydb.cursor()

app = Flask(__name__)

#New meeting insert için url.
@app.route('/insert/<data>')
def index(data):
    #Bu kısım datanın düzenlenmesi için.
    data = f'{data}'
    data = data.split("&")
    print(data)
    Topic = data[0]
    Date = "2021"+"-"+data[2]+"-"+data[1]
    StartTime = data[3]+":"+data[4]
    EndTime = data[5]+":"+data[6]
    Participants = data[7]
    sql = "INSERT INTO meetings (MeetingTopic, MeetingDate, MeetingTimeStart, MeetingTimeEnd, MeetingParticipants) VALUES (%s, %s, %s, %s, %s)"
    val = (Topic, Date, StartTime,EndTime,Participants)
    mycursor.execute(sql, val)
    mydb.commit()
    response = jsonify(message=data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

#Meeting listesi için
@app.route('/get/getmeetings')
def getmeetings():
    today = datetime.today()
    d1 = today.strftime("%Y-%m-%d")
    print(d1)
    mycursor.execute("SELECT * FROM meetings WHERE `MeetingDate` >= '"+d1+"' ORDER BY MeetingDate ASC")
    myresult = mycursor.fetchall()
    data = {}
    y = 0
    #Json formatına kolay çevirlmesi için dictionary kullanıldı
    for x in myresult:
        data[y] = {
            "ID" : x[0],
            "Topic" : x[1],
            "Date" : str(x[2]),
            "Start" : x[3],
            "End" : x[4],
            "Participants" : x[5]
        }
        y=y+1
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

#edit buttonuna tıklandığında datanın serverdan çekilip edit formuna gönderilmesi için.
@app.route('/edit/<id>')
def edit(id):
    id = f'{id}'
    mycursor.execute("SELECT * FROM meetings WHERE MeetingID =" +id)
    myresult = mycursor.fetchall()
    y = 0
    for x in myresult:
        day = x[2].strftime("%d")
        month = x[2].strftime("%m")
        start = x[3].split(":")
        print(start[0])
        end = x[4].split(":")
        print(end[0])
        data = {
            "ID" : x[0],
            "Topic" : x[1],
            "Date1" : day,
            "Date2" : month,
            "Start1" : start[0],
            "Start2": start[1],
            "End1" : end[0],
            "End2": end[1],
            "Participants" : x[5]
        }
        print(data)
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

#Update buttonu
@app.route('/update/<data>')
def update(data):
    #Datanın SQL database e gönderilmeden gerekli formatta düzenlenmesi.
    data = f'{data}'
    data = data.split("&")
    mycursor = mydb.cursor()
    Date = "2021"+"-"+data[2]+"-"+data[1]
    print(Date)
    StartTime = data[3]+":"+data[4]
    EndTime = data[5]+":"+data[6]
    sql = "UPDATE meetings SET MeetingTopic='"+data[0]+"', MeetingDate='"+Date+"', MeetingTimeStart='"+StartTime+"', MeetingTimeEnd='"+EndTime+"', MeetingParticipants='"+data[7]+"' WHERE MeetingID="+data[8]+""
    mycursor.execute(sql)
    mydb.commit()
    response = jsonify(message="Success")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

#Delete buttonu.
@app.route('/delete/<data>')
def delete(data):
    id = f'{data}'
    sql = "DELETE FROM meetings WHERE MeetingID = "+id+""
    mycursor.execute(sql)
    mydb.commit()
    response = jsonify(message="Success")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response