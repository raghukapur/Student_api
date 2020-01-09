import flask
import sqlite3
from flask import Flask
from flask import request
import simplejson

app = Flask(__name__)

@app.route('/data')
def get_data():
    if request.method=="GET":
        database=sqlite3.connect('student.db')
        cur=database.cursor()
        try:
            cur.execute("SELECT * FROM STUDENT")
            records=cur.fetchall()
            print("Total number of students in the table is: ", cur.rowcount)
            print("\nPrinting each student record")
            student_details = []
            for row in records:
                student_details = {
                    'SID' : row[0],
                    'FIRSTNAME' : row[1],
                    'LASTNAME' : row[2],
                    'PHONE NUMBER':row[3]}
                student_details.append(student_details)
            database.commit()
            database.close()
            return(simplejson.dumps(student_details))
        except:
            database.rollback()
            database.close()
            return("CONNECTION ERROR")
    else:
        return("REQUEST TYPE ERROR")


@app.route('/getspecific')
def get_specific():
    if request.method=="GET":
        database=sqlite3.connect('student.db')
        cur=database.cursor()
        print("hello")
        try:
            data=request.json
            if "sid" not in data:
                return("sid is not entered in the request")
            cur=database.cursor()
            cur.execute("SELECT * FROM STUDENT WHERE SID=={}".format(data["sid"]))
            details=cur.fetchone()
            if(details==None):
                print("no corrosponding SID in the table")
            else:
                return([{
                    'SID' : details[0],
                    'FIRSTNAME' : details[1],
                    'LASTNAME' : details[2],
                    'PHONE NUMBER':details[3]}])
                #print("SID = ", details[0], )
                #print("FIRSTNAME = ", details[1])
                #print("LASTNAME  = ", details[2])
                #print("PHONE NUMBER  = ", details[3], "\n")
            database.commit()
            database.close()
            #return ("The corrosponding details are correctly retrieved from the table")
        except:
            database.rollback()
            database.close()
            return("failure")
    else:
        return("Wrong Request type")

@app.route('/insertdata',methods=['POST'])
def insert_data():
    if request.method=="POST":
        database=sqlite3.connect('student.db')
        cur=database.cursor()
        try:
            details=request.json
            cur=database.cursor()
            if "sid" not in details or "lastname" not in details or "firstname" not in details or "phonenumber" not in details:
                return("All parameters are not passed in the request")
            try:
                cur.execute("INSERT INTO STUDENT VALUES({},'{}','{}',{});".format(int(details["sid"]),details["firstname"],details["lastname"],int(details["phonenumber"])))
            except:
                print("Data is not in the format")
                return("error while inserting the entry to the table")
            database.commit()
            database.close()
            return ("success message")
        except:
            database.rollback()
            database.close()
            return("failure")
    else:
        return("Wrong Request type")


@app.route('/deletespecific',methods=['DELETE'])
def delete_specific():
    if request.method=="DELETE":
        database=sqlite3.connect('student.db')
        cur=database.cursor()
        try:
            details=request.json
            cur=database.cursor()
            cur.execute("DELETE  FROM STUDENT WHERE SID={}".format(details["sid"]))
            while(True):
                detail=cur.fetchone()
                if detail==None:
                    break
                print(detail)
            database.commit()
            database.close()
            return ("ENTRY IN DELETED FROM THE TABLE")
        except:
            database.rollback()
            database.close()
            return("failure")
    else:
        return("Wrong Request type")

@app.route('/updatespecific',methods=['PUT'])
def update_specific():
    if request.method=="PUT":
        database=sqlite3.connect('student.db')
        cur=database.cursor()
        try:
            data=request.json
            cur=database.cursor()
            if "sid" not in data:
                return("sid is necessary for updates")
            if "firstname" in data:
                cur.execute("update STUDENT SET  FIRST_NAME='{}' WHERE SID={};".format(data["firstname"],int(data["sid"])))
            if "lastname" in data:
                cur.execute("update STUDENT SET  LAST_NAME='{}'where SID={};".format(data["lastname"],int(data["sid"])))
            if "phonenumber" in data:
                cur.execute("update STUDENT SET  PHONE_NUMBER={} WHERE SID={};".format(int(data["phonenumber"]),int(data["sid"])))
            database.commit()
            database.close()
            return ("ENTRY IN UPDATED FROM THE TABLE")
        except:
            database.rollback()
            database.close()
            return("failure")
    else:
        return("Wrong Request type")


if __name__ == '__main__':
    app.run(debug=True)
    
