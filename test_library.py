import unittest
import tkinter as tk
from main import LibraryApp

class TestLibraryApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = LibraryApp(self.root)

    def test_add_book(self):
        self.app.book_title_entry.insert(0, "The Lord of the Rings")
        self.app.book_author_entry.insert(0, "J.R.R. Tolkien")
        self.app.add_book()
        self.assertIn("The Lord of the Rings", self.app.books_tree.item(self.app.books_tree.get_children()[-1])['values'])

    def test_add_member(self):
        self.app.member_name_entry.insert(0, "John Doe")
        self.app.member_email_entry.insert(0, "john.doe@example.com")
        self.app.add_member()
        self.assertIn("John Doe", self.app.members_tree.item(self.app.members_tree.get_children()[-1])['values'])

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
