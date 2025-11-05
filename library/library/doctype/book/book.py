import frappe
from frappe.model.document import Document

class Book(Document):
    def validate(self):
        if not self.book_title:
            frappe.throw("Book title is required.")
        if not self.publisher:
            frappe.throw("Publisher is required.")
        if not self.category__genre:
            frappe.throw("Category is required.")
        if frappe.db.exists("Book", {
            "book_title": self.book_title,
            "publisher": self.publisher,
            "name": ["!=", self.name]
        }):
            frappe.throw("Book with this title and publisher already exists.")


def on_trash(self):
    if frappe.db.exists("Book", {"author": self.name}):
        frappe.throw("Cannot delete author linked to existing books.")
