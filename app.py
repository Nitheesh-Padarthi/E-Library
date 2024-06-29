from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
import requests

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['e_library']
borrowed_books = db['borrowed_books']

# Google Books API
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes?q="

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        response = requests.get(GOOGLE_BOOKS_API_URL + query)
        books = response.json().get('items', [])
        return render_template('results.html', books=books)
    return redirect(url_for('home'))

@app.route('/borrow/<book_id>', methods=['GET', 'POST'])
def borrow(book_id):
    if request.method == 'POST':
        user = request.form.get('user')
        borrowed_books.insert_one({'user': user, 'book_id': book_id})
        return redirect(url_for('home'))
    book = requests.get(f"https://www.googleapis.com/books/v1/volumes/{book_id}").json()
    return render_template('borrow.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)
