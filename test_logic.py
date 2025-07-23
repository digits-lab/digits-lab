import unittest
import sqlite3
from database import create_tables

class TestLibraryLogic(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            status TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowed_books (
            id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            issue_date DATE NOT NULL,
            return_date DATE,
            FOREIGN KEY (book_id) REFERENCES books (id),
            FOREIGN KEY (member_id) REFERENCES members (id)
        )
        ''')

        self.conn.commit()

    def test_add_book(self):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO books (title, author, status) VALUES (?, ?, ?)", ("The Lord of the Rings", "J.R.R. Tolkien", 'Available'))
        self.conn.commit()
        cursor.execute("SELECT * FROM books")
        self.assertEqual(len(cursor.fetchall()), 1)

    def test_add_member(self):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO members (name, email) VALUES (?, ?)", ("John Doe", "john.doe@example.com"))
        self.conn.commit()
        cursor.execute("SELECT * FROM members")
        self.assertEqual(len(cursor.fetchall()), 1)

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
