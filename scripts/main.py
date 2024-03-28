from pywebio.input import *
from pywebio.output import *
from flask import Flask
from pywebio.platform.flask import webio_view
import event_management as Ae
import book_ticket as Bt

app = Flask(__name__)

def main():
    choice = radio("Select Your choice: ", options=["Event manager", "Book a ticket"])
    if choice == "Event manager":
        choice = radio("Select Your choice: ", options=["Add event", "See Bookings"])
        if choice == "Add event":
            Ae.create()
        else:
            Ae.see_booking()
    else:
        Bt.book()

app.add_url_rule('/', 'webio_view', webio_view(main), methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run(debug=False)

