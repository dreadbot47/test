from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'simple_secret_key'

# In-memory storage for books
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "status": "Available"},
    {"id": 2, "title": "1984", "author": "George Orwell", "status": "Borrowed"}
]

@app.route('/')
def index():
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    
    if not title or not author:
        flash("Fill all fields", "error")
    else:
        new_id = len(books) + 1
        books.append({
            "id": new_id,
            "title": title,
            "author": author,
            "status": "Available"
        })
        flash("Book added!", "success")
    return redirect(url_for('index'))

@app.route('/borrow_book/<int:book_id>')
def borrow_book(book_id):
    for book in books:
        if book['id'] == book_id:
            book['status'] = "Borrowed"
            flash(f"Book '{book['title']}' borrowed", "success")
            break
    return redirect(url_for('index'))

@app.route('/return_book/<int:book_id>')
def return_book(book_id):
    for book in books:
        if book['id'] == book_id:
            book['status'] = "Available"
            flash(f"Book '{book['title']}' returned", "success")
            break
    return redirect(url_for('index'))

@app.route('/check_availability', methods=['POST'])
def check_availability():
    query = request.form.get('title', '').strip().lower()
    
    for book in books:
        if book['title'].lower() == query:
            flash(f"Book '{book['title']}' status: {book['status']}", "info")
            return redirect(url_for('index'))
            
    flash("Not Found", "error")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)