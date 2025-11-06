import frappe
from frappe.model.document import Document
from frappe.utils import add_days, add_months, nowdate

class LibraryTransaction(Document):
    def before_insert(self):
        """Automatically issue the book when record is created (default status = Issued)"""
        if self.status != "Issued":
            return

        # 1️⃣ Check if the book has available copies
        book = frappe.get_doc("Book", self.book)
        if book.available_copies < 1:
            frappe.throw("No copies available for this book.")

        # 2️⃣ Check member limit
        max_limit = 3
        current_borrowed = frappe.db.count(
            "Library Transaction",
            {
                "member": self.member,
                "status": "Issued"
            }
        )

        if current_borrowed >= max_limit:
            frappe.throw(f"Member has reached the maximum allowed borrowed books ({max_limit}).")
    def after_insert(self):
        """Update book availability and set due date after issuing the book"""

        book = frappe.get_doc("Book", self.book)
        # 3️⃣ Reduce available copies
        book.available_copies -= 1
        book.save(ignore_permissions=True)

        # 4️⃣ Calculate due date
        issue_date = self.issue_date or nowdate()
        duration = (self.borrow_duration or "").strip().lower()

        if "week" in duration:
            weeks = int(duration.split()[0])
            self.due_date = add_days(issue_date, weeks * 7)
        elif "month" in duration:
            months = int(duration.split()[0])
            self.due_date = add_months(issue_date, months)
        else:
            self.due_date = add_days(issue_date, 7)

        # 5️⃣ Save updated info
        self.issue_date = issue_date
        self.save(ignore_permissions=True)

        frappe.msgprint(f"Book '{self.book}' issued to member '{self.member}'. Due date: {self.due_date}")


@frappe.whitelist()
def return_book(docname):
    """Return book manually"""
    doc = frappe.get_doc("Library Transaction", docname)
    if doc.status == "Returned":
        frappe.throw("Book already returned.")

    book = frappe.get_doc("Book", doc.book)
    book.available_copies += 1
    book.save(ignore_permissions=True)

    doc.status = "Returned"
    doc.return_date = nowdate()
    doc.save(ignore_permissions=True)

    frappe.msgprint(f"Book '{doc.book}' returned successfully.")


def update_overdue_transactions():
    today = nowdate()
    overdue_transactions = frappe.get_all(
        "Library Transaction",
        filters={"status": "Issued", "due_date": ("<", today)},
        fields=["name"],
    )

    for tx in overdue_transactions:
        frappe.db.set_value("Library Transaction", tx.name, "status", "Overdue")

    frappe.db.commit()
    frappe.logger().info(f"Updated {len(overdue_transactions)} overdue transactions.")

# أنا بصنع Library Management App باستخدام Frappe Framework.
# لحد دلوقتي عملت الـ Doctypes التالية:

# Book (fields: title, category, publisher, authors, total_copies, available_copies)

# Author

# Publisher

# Category / Genre

# Book Author (Child Table linking Book & Author)

# Library Transaction (Submittable, fields: member, book, issue_date, return_date, status, remarks)

# لحد دلوقتي أضفت backend logic لتحديث available_copies عند الاستعارة (submit) والإرجاع (cancel)، وكمان تحققنا من الحد الأقصى للاستعارة للعضو.

# أريدك تكمل معي تطوير الـ app:

# إضافة dashboard أو واجهة عرض للكتب المتاحة والمعاملات.

# إضافة منطق ذكي Overdue Detection: تلقائيًا تغير حالة المعاملة لو الكتاب متأخر عن موعد الإرجاع.

# إضافة إمكانية بحث وفلترة الكتب حسب المؤلف، الناشر، أو التصنيف.

# أرجو أن تبدأ بالكود أو الاقتراحات المباشرة لتطبيق هذه الميزات داخل Frappe/Python.
