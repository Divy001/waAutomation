from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "hh")
    response = MessagingResponse()
    msg = response.message(f"Thanks for contacting me. You Have sent '{text}' from '{number}' ")
    #msg = response.message("Hello Divy This Event Poster for the Event ")
    #msg.media("https://events-webapp.s3.ap-south-1.amazonaws.com/event_images/FGR%20Awareness%20December%20.png")

    return str(response)

if __name__ == "__main__":
    app.run(port=5000)
