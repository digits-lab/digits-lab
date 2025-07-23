import tkinter as tk
from tkinter import ttk
import sqlite3

def create_connection():
    conn = sqlite3.connect('library.db')
    return conn

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")

        self.conn = create_connection()
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, expand=True, fill='both')

        self.create_books_tab()
        self.create_members_tab()
        self.create_borrow_tab()

    def create_books_tab(self):
        self.books_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.books_frame, text='Books')

        ttk.Label(self.books_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.book_title_entry = ttk.Entry(self.books_frame)
        self.book_title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.books_frame, text="Author:").grid(row=1, column=0, padx=5, pady=5)
        self.book_author_entry = ttk.Entry(self.books_frame)
        self.book_author_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_book_button = ttk.Button(self.books_frame, text="Add Book", command=self.add_book)
        self.add_book_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.books_tree = ttk.Treeview(self.books_frame, columns=('ID', 'Title', 'Author', 'Status'), show='headings')
        self.books_tree.heading('ID', text='ID')
        self.books_tree.heading('Title', text='Title')
        self.books_tree.heading('Author', text='Author')
        self.books_tree.heading('Status', text='Status')
        self.books_tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.load_books()

    def create_members_tab(self):
        self.members_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.members_frame, text='Members')

        ttk.Label(self.members_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.member_name_entry = ttk.Entry(self.members_frame)
        self.member_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.members_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.member_email_entry = ttk.Entry(self.members_frame)
        self.member_email_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_member_button = ttk.Button(self.members_frame, text="Add Member", command=self.add_member)
        self.add_member_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.members_tree = ttk.Treeview(self.members_frame, columns=('ID', 'Name', 'Email'), show='headings')
        self.members_tree.heading('ID', text='ID')
        self.members_tree.heading('Name', text='Name')
        self.members_tree.heading('Email', text='Email')
        self.members_tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.load_members()

    def create_borrow_tab(self):
        self.borrow_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.borrow_frame, text='Borrow Books')

        ttk.Label(self.borrow_frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5)
        self.borrow_book_id_entry = ttk.Entry(self.borrow_frame)
        self.borrow_book_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.borrow_frame, text="Member ID:").grid(row=1, column=0, padx=5, pady=5)
        self.borrow_member_id_entry = ttk.Entry(self.borrow_frame)
        self.borrow_member_id_entry.grid(row=1, column=1, padx=5, pady=5)

        self.borrow_button = ttk.Button(self.borrow_frame, text="Borrow Book", command=self.borrow_book)
        self.borrow_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.borrowed_tree = ttk.Treeview(self.borrow_frame, columns=('ID', 'Book ID', 'Member ID', 'Issue Date', 'Return Date'), show='headings')
        self.borrowed_tree.heading('ID', text='ID')
        self.borrowed_tree.heading('Book ID', text='Book ID')
        self.borrowed_tree.heading('Member ID', text='Member ID')
        self.borrowed_tree.heading('Issue Date', text='Issue Date')
        self.borrowed_tree.heading('Return Date', text='Return Date')
        self.borrowed_tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.load_borrowed_books()

    def add_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        if title and author:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO books (title, author, status) VALUES (?, ?, ?)", (title, author, 'Available'))
            self.conn.commit()
            self.load_books()
            self.book_title_entry.delete(0, tk.END)
            self.book_author_entry.delete(0, tk.END)

    def load_books(self):
        for i in self.books_tree.get_children():
            self.books_tree.delete(i)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM books")
        for row in cursor.fetchall():
            self.books_tree.insert('', 'end', values=row)

    def add_member(self):
        name = self.member_name_entry.get()
        email = self.member_email_entry.get()
        if name and email:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
            self.conn.commit()
            self.load_members()
            self.member_name_entry.delete(0, tk.END)
            self.member_email_entry.delete(0, tk.END)

    def load_members(self):
        for i in self.members_tree.get_children():
            self.members_tree.delete(i)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM members")
        for row in cursor.fetchall():
            self.members_tree.insert('', 'end', values=row)

    def borrow_book(self):
        book_id = self.borrow_book_id_entry.get()
        member_id = self.borrow_member_id_entry.get()
        if book_id and member_id:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO borrowed_books (book_id, member_id, issue_date) VALUES (?, ?, date('now'))", (book_id, member_id))
            cursor.execute("UPDATE books SET status = 'Borrowed' WHERE id = ?", (book_id,))
            self.conn.commit()
            self.load_borrowed_books()
            self.load_books()
            self.borrow_book_id_entry.delete(0, tk.END)
            self.borrow_member_id_entry.delete(0, tk.END)

    def load_borrowed_books(self):
        for i in self.borrowed_tree.get_children():
            self.borrowed_tree.delete(i)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM borrowed_books")
        for row in cursor.fetchall():
            self.borrowed_tree.insert('', 'end', values=row)

def main():
    root = tk.Tk()
    app = LibraryApp(root)

    # Add a book
    app.book_title_entry.insert(0, "The Lord of the Rings")
    app.book_author_entry.insert(0, "J.R.R. Tolkien")
    app.add_book()

    # Add a member
    app.member_name_entry.insert(0, "John Doe")
    app.member_email_entry.insert(0, "john.doe@example.com")
    app.add_member()

    # Borrow a book
    app.borrow_book_id_entry.insert(0, 1)
    app.borrow_member_id_entry.insert(0, 1)
    app.borrow_book()

    # Print the data
    print("Books:")
    app.load_books()
    print("\nMembers:")
    app.load_members()
    print("\nBorrowed Books:")
    app.load_borrowed_books()

    root.destroy()

if __name__ == '__main__':
    main()
