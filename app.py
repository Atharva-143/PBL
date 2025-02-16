from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message 
import smtplib
from datetime import datetime, timedelta

app = Flask(__name__)
mail = Mail(app)
app.secret_key = "your_secret_key"  # Required for session management

# Sample user data
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'user1': {'password': 'user123', 'role': 'user'}
}

# Sample data for 50 books with images
books = [
    {"id": 1, "title": "Ramayana", "author": "Shree Valmiki", "available": True, "image": "book1.jpg"},
    {"id": 2, "title": "Mahabharat", "author": "Shree Veda Vyasa", "available": True, "image": "book2.jpg"},
    {"id": 3, "title": "Bhagwat Geeta", "author": "Shree krishna", "available": True, "image": "book3.jpg"},
    {"id": 4, "title": "The Guide ", "author": "R.K Narayan", "available": True, "image": "book4.jpg"},
    {"id": 5, "title": "Malgudi Days", "author": "R.K Narayan", "available": True, "image": "book5.jpg"},
    {"id": 6, "title": "Midnight's children", "author": "Salman Rushidie", "available": True, "image": "book6.jpg"},
    {"id": 7, "title": "A Suitable Boy", "author": "Vikram seth ", "available": True, "image": "book7.jpg"},
    {"id": 8, "title": "Train to Pakistan", "author": "Khusawant singh", "available": True, "image": "book8.jpg"},
    {"id": 9, "title": "Gitanjali", "author": "Rabindranath tagore", "available": True, "image": "book9.jpg"},
    {"id": 10, "title": "The Shadow lines", "author": "Amitav Ghosh", "available": True, "image": "book10.jpg"},
    {"id": 11, "title": "The Glass Palace", "author": "Amitav Ghosh", "available": True, "image": "book11.jpg"},
    {"id": 12, "title": "Kanthapura", "author": "Raja Rao", "available": True, "image": "book12.jpg"},
    {"id": 13, "title": "Godan", "author": "Musnhi Premchand", "available": True, "image": "book13.jpg"},
    {"id": 14, "title": "The God of small things", "author": "Arundhati Roy", "available": True, "image": "book14.jpg"},
    {"id": 15, "title": "The White Tiger", "author": "Aravind Adiga", "available": True, "image": "book15.jpg"},
    {"id": 16, "title": "The Inheritance of Loss", "author": "Kiran desai", "available": True, "image": "book16.jpg"},
    {"id": 17, "title": "The Namesake", "author": "Jhumpa lahiri", "available": True, "image": "book17.jpg"},
    {"id": 18, "title": "Interpretor of Maldives", "author": "Amitav Ghosh", "available": True, "image": "book18.jpg"},
    {"id": 19, "title": "The Lowland", "author": "jhumpa lahari", "available": True, "image": "book19.jpg"},
    {"id": 20, "title": "Sea of poppies", "author": "Amitav Gurav", "available": True, "image": "book20.jpg"},
    {"id": 21, "title": "The Hungary Tide", "author": "Shashi Tharoor", "available": True, "image": "book21.jpg"},
    {"id": 22, "title": "The great Indian Novel", "author": "Chitra Banerjeee Divakaruni", "available": True, "image": "book22.jpg"},
    {"id": 23, "title": "The palace of Illusions", "author": "Amish Tripathi", "available": True, "image": "book23.jpg"},
    {"id": 24, "title": "The immortals of Mehula", "author": "Amish Tripathi", "available": True, "image": "book24.jpg"},
    {"id": 25, "title": "The secret of Nagas", "author": "Arundhati Roy", "available": True, "image": "book25.jpg"},
    {"id": 26, "title": "The Oath of Vayuputras", "author": "Devanki Nandan Khatri", "available": True, "image": "book26.jpg"},
    {"id": 27, "title": "The Ministry of Utmost Happiness", "author": "Bhisham Sahni", "available": True, "image": "book27.jpg"},
    {"id": 28, "title": "Chandrakanta", "author": "Munshi Premchand", "available": True, "image": "book28.jpg"},
    {"id": 29, "title": "Raag Darbari", "author": "V.S Khandekar", "available": True, "image": "book29.jpg"},
    {"id": 30, "title": "Tamas", "author": "Sanskar", "available": True, "image": "book30.jpg"},
    {"id": 31, "title": "Gaban", "author": "Yashpal", "available": True, "image": "book31.jpg"},
    {"id": 32, "title": "Yayati", "author": "Bibhutibhushan Bandyopadhyay", "available": True, "image": "book32.jpg"},
    {"id": 33, "title": "Chowringhee", "author": "Ramchandra Guha", "available": True, "image": "book33.jpg"},
    {"id": 34, "title": "Jhootha Sach", "author": "Amartya Sen", "available": True, "image": "book34.jpg"},
    {"id": 35, "title": "Pather Panchali", "author": "Bhagat singh ", "available": True, "image": "book35.jpg"},
    {"id": 36, "title": "India after Gandhi", "author": "Shashi Tharoor", "available": True, "image": "book36.jpg"},
    {"id": 37, "title": "The Argumentative Indian", "author": "Mahatma gandhi", "available": True, "image": "book37.jpg"},
    {"id": 38, "title": "Why I am an Atheist", "author": "A.P.J Abdul Kalam ", "available": True, "image": "book38.jpg"},
    {"id": 39, "title": "An era of Darkness", "author": "Sachin Tendulkar", "available": True, "image": "book39.jpg"},
    {"id": 40, "title": "The Story of my Experiments with Truth", "author": "Sagarika Ghose", "available": True, "image": "book40.jpg"},
    {"id": 41, "title": "Wings of fire", "author": "Raghuram Rajan", "available": True, "image": "book41.jpg"},
    {"id": 42, "title": "Playing it my way", "author": "Sri Aurobindo", "available": True, "image": "book42.jpg"},
    {"id": 43, "title": "Indira:India's Most Powerful Prime Minister", "author": "A.C Bhatikvenda Swami Prabhupada", "available": True, "image": "book43.jpg"},
    {"id": 44, "title": "I Do What I Do", "author": "Swami Vivekanada", "available": True, "image": "book44.jpg"},
    {"id": 45, "title": "Savitri", "author": "Various Author", "available": True, "image": "book45.jpg"},
    {"id": 46, "title": "Autobiography of a Yogi", "author": "Eknath Easwaram", "available": True, "image": "book46.jpg"},
    {"id": 47, "title": "The complete works of Swami vivekananda", "author": "Swami vivekanada", "available": True, "image": "book47.jpg"},
    {"id": 48, "title": "Speaking Tree: A collection of Spiritual writings", "author": "Various Authors", "available": True, "image": "book48.jpg"},
    {"id": 49, "title": "The upanishads", "author": "eknath easwaran", "available": True, "image": "book49.jpg"},
    {"id": 50, "title": "Chanakya Neeti", "author": "Vishnu Sharma", "available": True, "image": "book50.jpg"},
]

# Dictionary to store borrowed books and their due dates
borrowed_books = {}

# Email configuration
EMAIL_ADDRESS = "bagwanasad36@gmail.com"
EMAIL_PASSWORD = "ABC"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(to_email, subject, body):
    try:
        # Using the Gmail SMTP server
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            # Login using the email address and app password
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            
            # Constructing the email message
            message = f"Subject: {subject}\n\n{body}"
            
            # Sending the email
            server.sendmail(EMAIL_ADDRESS, to_email, message)
        
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def borrow_book(user_email, book_id, days):
    book = next((b for b in books if b["id"] == book_id), None)
    if book and book["available"]:
        book["available"] = False
        due_date = datetime.now() + timedelta(days=days)
        borrowed_books[book_id] = {"user_email": user_email, "due_date": due_date}
        print(f"Book '{book['title']}' borrowed successfully. Due date: {due_date.strftime('%Y-%m-%d')}")
    else:
        print("Book not available or does not exist.")

def return_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book and not book["available"]:
        book["available"] = True
        borrowed_info = borrowed_books.pop(book_id, None)
        if borrowed_info:
            print(f"Book '{book['title']}' returned successfully.")
    else:
        print("Book not borrowed or does not exist.")

def check_due_dates():
    today = datetime.now()
    for book_id, info in borrowed_books.items():
        if info["due_date"] - today <= timedelta(days=2):
            book = next((b for b in books if b["id"] == book_id), None)
            if book:
                subject = "Reminder: Book Due Soon"
                body = f"Dear User,\n\nThis is a reminder that the book '{book['title']}' is due on {info['due_date'].strftime('%Y-%m-%d')}. Please return it on time.\n\nThank you!"
                send_email(info["user_email"], subject, body)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.get(username)
        if user and user['password'] == password:
            session["username"] = username
            if user['role'] == 'admin':
                session["admin"] = True
                return redirect(url_for("admin"))
            return redirect(url_for("list_books"))  # Redirect regular users to the book list
        else:
            flash("Invalid credentials. Please try again.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("admin", None)  # Also pop the admin session variable
    return redirect(url_for("index"))

@app.route("/list")
def list_books():
    return render_template("list.html", books=books)

@app.route("/borrow", methods=["GET", "POST"])
def borrow():
    if request.method == "POST":
        user_email = request.form["email"]
        book_id = int(request.form["book_id"])
        days = int(request.form["days"])
        book = next((b for b in books if b["id"] == book_id), None)
        if book and book["available"]:
            borrow_book(user_email, book_id, days)
            flash(f"Book '{book['title']}' borrowed successfully.")
        else:
            flash("Book not available or does not exist.")
        return redirect(url_for("list_books"))
    return render_template("borrow.html")

@app.route("/return", methods=["GET", "POST"])
def return_book_route():
    if request.method == "POST":
        book_id = int(request.form["book_id"])
        return_book(book_id)
        return redirect(url_for("list_books"))
    return render_template("return.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "admin" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        check_due_dates()
        return redirect(url_for("admin"))
    return render_template("admin.html", borrowed_books=borrowed_books, books=books)

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'username' not in session or users[session['username']]['role'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html', borrowed_books=borrowed_books)

@app.route('/admin/send_reminder/<int:book_id>', methods=['GET', 'POST'])
def send_reminder(book_id):
    if 'username' not in session or users[session['username']]['role'] != 'admin':
        return redirect(url_for('login'))

    borrowed_info = borrowed_books.get(book_id)
    if not borrowed_info:
        flash('Book not found or not borrowed')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        user_email = borrowed_info['user_email']
        book = next((b for b in books if b["id"] == book_id), None)
        if book:
            subject = "Reminder: Book Due Soon"
            body = f"Dear User,\n\nThis is a reminder that the book '{book['title']}' is due soon. Please return it on time.\n\nThank you!"
            send_email(user_email, subject, body)
            flash(f'Reminder sent to {user_email} to return {book["title"]}')
            return redirect(url_for('admin_dashboard'))
    return render_template('send_reminder.html', book=book)


if __name__ == "__main__":
    app.run(debug=True)
