import pyodbc

from flask import Flask,jsonify,request

app=Flask(__name__)


try:
    connection_string = pyodbc.connect("Driver={SQL Server};"
            "Server=DESKTOP-LAT9O91;"
            "Database=SQL Training;"
            "Trusted_Connection=yes;")
    cursor=connection_string.cursor()
    print("connected to SQL server")

except pyodbc.Error as e:
    print("error occured")

@app.route("/")
def home():
    return "Hello world"

@app.route("/Get_customer", methods=["GET"])
def get_customer():
       try:
          cursor.execute("SELECT * FROM Customers Table")
          list=cursor.fetchall()
          data=[]
          for i in list:
              a={"CustomerID":i[0],"FirstName":i[1],"LastName":i[2],"RegistrationDate":i[3]}
              data.append(a)
          print(data)
          return jsonify({"data":data})
       except pyodbc.Error as e:
            print(f"error:{e}")
            return jsonify({"message":f"error occured:{e}"})
       
    
@app.route("/create_customer",methods=["POST"])
def create_Customer():
       try:
          firstname=request.json.get('firstname')
          lastname=request.json.get('lastname')
          registrationdate=request.json.get('registrationdate')

          if firstname !="" and lastname !=""and registrationdate !="":
              cursor.execute("Insert Into Customer Table(FirstName,LastName,RegistrationDate) VALUES (?,?,?)",(firstname,lastname,registrationdate))
              connection_string.commit()
              return jsonify({"message":"Customer Table created Succesfully"})
          else:
              return jsonify({"message":"Error occured"})
       
       except pyodbc.Error as e:
           print(f"error:{e}")
           return jsonify({"message":f"Error occured:{e}"})

    
@app.route("/update_Customer/<int:CustomerID>",methods=["PUT"])
def update_Customer(CustomerID):
        try:
            firstname =request.json.get("firstname")
            lastname =request.json.get("lastname")
            registrationdate =request.json.get("registrationdate")

            if firstname and lastname and registrationdate:
                cursor.execute("UPDATE Customer Table SET FirstName=?,LastName=?,RegistrationDtae=? WHERE CustomerID=?",(firstname,lastname,registrationdate))
                connection_string.commit()
                return jsonify({"message":"Updated Succesfully"})
            else:
                return jsonify({"message":"All data  is required"})
            
        except pyodbc.Error as e:
            print(f"error:{e}")
            return jsonify({"message":f"error:{e}"})
        


@app.route("/delete_data/<int:id>", methods=["DELETE"])
def delete_author(id):
    if conn and cursor:
        try:
            cursor.execute("DELETE FROM authors WHERE id=?",(id))
            conn.commit()
            return jsonify({"message":"Deleted Sucesfully"})
        except pyodbc.Error as er:
            print(f"error:{er}")
            return jsonify({"message":f"Something went wrong:{er}"})
    else:
        return jsonify({"message":"Please connect database"})



if __name__=='__main__':
    app.run(host="localhost",port=5000,debug=True)



  



