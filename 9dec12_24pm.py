from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime
import certifi

#cluster = MongoClient("mongodb+srv://divy:divy@cluster0.asioc.mongodb.net/?retryWrites=true&w=majority")
cluster = MongoClient("mongodb+srv://hcpwire:hcpwire@cluster0.osnlh.mongodb.net/test")
#mongodb+srv://hcpwire:hcpwire@cluster0.osnlh.mongodb.net/test
db = cluster["retail-corporate-testing"]
users = db["ppmcs"]
appointments = db["appointments"]

app = Flask(__name__)

#data = users.find_one({},{"_id":0, "patientName":1,"patientPhone":1, "patientAddress":1, "patientPincode":1})
#print(data["patientName"])


@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")
    number = number[3:]
    response = MessagingResponse()
    findNum = { "patientPhone": "9886259672" }
    #data = users.find(findNum, {"_id": 0, "patientName": 1, "patientPhone": 1, "patientAddress": 1, "patientPincode": 1})
    data = users.find_one(findNum,{"_id": 0, "patientName": 1, "patientPhone": 1, "patientAddress": 1, "patientPincode": 1})
    print(data)
    print(findNum)
    print(number)
    name = data.get("patientName")
    mobile = data.get("patientPhone")
    address = data.get("patientAddress")
    pincode = data.get("patientPincode")

    user = users.find_one(findNum)
    #user = "true"
    #if bool(user) == False:
    if "hi" in text:
        response.message("Hey, Type 'book' to Proceed Further.")
    elif "book" in text and bool(user) == True:
        response.message(f" Hi  ! You're required to undergo a Pre-Policy Health Check(PPHC) as a part of your policy purchase with ACKO Insurance.\nFor next steps, we will help you with your booking for the PPHC. Kindly confirm/update the below information we've received from ACKO, to plan and confirm your PPHC.\n \n Name: {name} \n Mobile Number: {mobile} \n Address: {address} \n Pincode: {pincode}\n\n\n ➡️What would you like to do? \n\n 1️⃣Update These Details. \n 2️⃣Keep These Details.\n 3️⃣Customer Support Number")
        appointments.insert_one({"number": mobile, "status": "main", "messages": []})
    elif "book" in text and bool(user) == False:
        response.message(f" Hi  ! You're required to undergo a Pre-Policy Health Check(PPHC) as a part of your policy purchase with ACKO Insurance.\nFor next steps, we will help you with your booking for the PPHC. Kindly confirm/update the below information we've received from ACKO, to plan and confirm your PPHC.\n \n Name: {name}  \n Mobile Number: {mobile} \n Address: {address} \n Pincode: {pincode} \n\n\n ➡️What would you like to do? \n\n 1️⃣Update These Details. \n 2️⃣Keep These Details.\n 3️⃣Customer Support Number")
        appointments.update_one({"number": mobile}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})

    return str(response)


if __name__ == "__main__":
    app.run(port=5000)
    
    
    
#14 Dec 2022

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime
import certifi

# cluster = MongoClient("mongodb+srv://divy:divy@cluster0.asioc.mongodb.net/?retryWrites=true&w=majority")
cluster = MongoClient("mongodb+srv://hcpwire:hcpwire@cluster0.osnlh.mongodb.net/test",tls=True, tlsAllowInvalidCertificates=True)
# mongodb+srv://hcpwire:hcpwire@cluster0.osnlh.mongodb.net/test
db = cluster["retail-corporate-testing"]
users = db["ppmcs"]
appointments = db["appointments"]

app = Flask(__name__)


# data = users.find_one({},{"_id":0, "patientName":1,"patientPhone":1, "patientAddress":1, "patientPincode":1})
# print(data["patientName"])


@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    # print(number)
    number = number.replace("whatsapp:", "")
    number = number[3:]
    response = MessagingResponse()
    findNum = {"patientPhone": number}
    # data = users.find(findNum, {"_id": 0, "patientName": 1, "patientPhone": 1, "patientAddress": 1, "patientPincode": 1})
    data = users.find_one(findNum,
                          {"_id": 0, "patientName": 1, "patientPhone": 1, "patientAddress": 1, "patientPincode": 1})
    # print(data)
    # print(findNum)
    # print(number)
    name = data.get("patientName")
    mobile = data.get("patientPhone")
    address = data.get("patientAddress")
    pincode = data.get("patientPincode")

    user = users.find_one(findNum)
    appointment = appointments.find_one({"number": mobile})
    print(appointment["status"])
    # print(appointment)

    # print(user)
    # user = "true"
    # if bool(user) == False:
    if "hi" in text:
        response.message("Hey, Type 'book' to Proceed Further.")
    if "book" in text:
        response.message(
            f" Hi  ! You're required to undergo a Pre-Policy Health Check(PPHC) as a part of your policy purchase with ACKO Insurance.\nFor next steps, we will help you with your booking for the PPHC. Kindly confirm/update the below information we've received from ACKO, to plan and confirm your PPHC.\n \n Name: {name} \n Mobile Number: {mobile} \n Address: {address} \n Pincode: {pincode}\n\n\n ➡️What would you like to do? \n\n 1️⃣Update These Details. \n 2️⃣Keep These Details.\n 3️⃣Customer Support Number")
        if bool(appointment) == False:
            appointments.insert_one({"number": mobile, "status": "main", "messages": []})
        else:
            appointments.update_one({"number": mobile}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    elif appointment["status"] == "main":
        try:
            global option
            option = int(text)
            print("option" + option)
        except:
            print("except")
            #except:
            #response.message("Enter A Valid Response", option)
            #return str(response)
        if option == 1:
            response.message("Lets *Update* Your Details!")
            appointments.update_one({"number": number}, {"$set": {"status": "updating"}})
            response.message(
                "Which details would you like to *Change*? \n Reply with the number of your choice.(For example, if you would like to change your first name, reply with the number 1) \n 1️⃣. *Name* \n 2️⃣. *Mobile Number* \n 3️⃣. *Address* \n 4️⃣. *Pincode*")

        elif option == 2:
            response.message(f"Thanks *{name}*! Your details have been saved 😀👍")
            response.message(
                "Your details for conducting the  Pre-Policy Medical Check required for your health insurance requirement with Acko has been updated. Would you like to proceed with the booking? \n Kindly enter '1' to proceed or '2' to remind you later.\n\n 1. Yes, proceed. \n 2. Remind me later")

        elif option == 3:
            response.message("Thanks for Choosing To Contact Us on +919448920370")

        else:
            response.message("Enter A Valid Response")
            return str(response)

    elif appointment["status"] == "updating":
        try:
            option = int(text)
        except:
            response.message("Enter a Valid Response")
            return str(response);
        if option == 1:
            response.message("Please reply with your name.")
            return str(response)
        if(text == "str"):
            global patientName
            patientName = users.update_one(findNum, {"$set": {"patientName": text}})
        elif type(text) == str:
            response.message("👍🏻Got it! \n Would you like to change any other details? \n\n Type 'Yes' or 'No'")
        if(text == "Yes"):
            response.message(
                    "Which details would you like to *Change*? \n Reply with the number of your choice.(For example, if you would like to change your first name, reply with the number 1) \n 1️⃣. *Name* \n 2️⃣. *Mobile Number* \n 3️⃣. *Address* \n 4️⃣. *Pincode*")
        elif(text == "No"):
            response.message(f"Thanks *{name}*! Your details have been saved 😀👍")
            response.message(
                    "Your details for conducting the  Pre-Policy Medical Check required for your health insurance requirement with Acko has been updated. Would you like to proceed with the booking? \n Kindly enter '1' to proceed or '2' to remind you later.\n\n 1. Yes, proceed. \n 2. Remind me later")
        else:
            response.message("Enter A Valid Response")
            return str(response)

        if option == 2:
            response.message("Please reply with your active mobile number for our team to reach you(intended test taker) at")
            if(text):
                users.update_one(findNum,{"$set": {"patientPhone": text}})



    return str(response)


if __name__ == "__main__":
    app.run(port=5000)

