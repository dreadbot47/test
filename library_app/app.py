from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flashing messages

# In-memory storage for books
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "status": "Available"},
    {"id": 2, "title": "1984", "author": "George Orwell", "status": "Borrowed"}
]

@app.route('/')
def index():
    search_query = request.args.get('search', '').lower()
    filtered_books = books
    if search_query:
        filtered_books = [b for b in books if search_query in b['title'].lower() or search_query in b['author'].lower()]
    return render_template('index.html', books=filtered_books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    
    if not title or not author:
        flash("Fill all fields!", "error")
    else:
        new_id = len(books) + 1
        books.append({
            "id": new_id,
            "title": title,
            "author": author,
            "status": "Available"
        })
        flash(f"Book '{title}' added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/borrow_book/<int:book_id>')
def borrow_book(book_id):
    for book in books:
        if book['id'] == book_id:
            if book['status'] == "Available":
                book['status'] = "Borrowed"
                flash(f"Book '{book['title']}' borrowed successfully!", "success")
            else:
                flash(f"Book '{book['title']}' is already borrowed.", "error")
            break
    return redirect(url_for('index'))

@app.route('/return_book/<int:book_id>')
def return_book(book_id):
    for book in books:
        if book['id'] == book_id:
            if book['status'] == "Borrowed":
                book['status'] = "Available"
                flash(f"Book '{book['title']}' returned successfully!", "success")
            else:
                flash(f"Book '{book['title']}' was not checked out.", "error")
            break
    return redirect(url_for('index'))

@app.route('/check_availability', methods=['POST'])
def check_availability():
    query = request.form.get('query', '').strip().lower()
    if not query:
        flash("Please enter a book title to check.", "error")
        return redirect(url_for('index'))
    
    found_books = [b for b in books if query in b['title'].lower()]
    if found_books:
        for b in found_books:
            flash(f"'{b['title']}' by {b['author']} is currently: {b['status']}", "info")
    else:
        flash(f"Book '{query}' Not Found.", "error")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)