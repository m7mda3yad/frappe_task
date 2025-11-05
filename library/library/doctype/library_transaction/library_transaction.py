from annotated_types import doc
import frappe
from frappe.model.document import Document
from frappe.utils import add_days, nowdate
from frappe.utils import nowdate
from frappe.utils import add_days, add_months, nowdate
class LibraryTransaction(Document):

    @frappe.whitelist()
    def return_book(self):
        if self.status == "Returned":
            frappe.throw("Book already returned.")
        book = frappe.get_doc("Book", self.book)
        book.available_copies += 1
        book.save()
        self.status = "Returned"
        self.return_date = nowdate()
        self.save()

        frappe.msgprint(f"Book '{self.book}' returned successfully.")




    def before_submit(self):
        # 1️⃣ Check if the book has available copies
        book = frappe.get_doc("Book", self.book)
        if book.available_copies < 1:
            frappe.throw("No copies available for this book.")

        # 2️⃣ Check the maximum allowed borrowed books for the member
        max_limit = 3
        current_borrowed = frappe.db.count("Library Transaction", {
            "member": self.member,
            "docstatus": 1,  # Submitted
            "status": "Issued"
        })

        if current_borrowed >= max_limit:
            frappe.throw(f"Member has reached the maximum allowed borrowed books ({max_limit}).")

        # 3️⃣ Reduce the available copies of the book
        book.available_copies -= 1
        book.save()

        self.status = "Issued"


        # 4️⃣ calc  borrow_duration
        issue_date = self.issue_date or nowdate()
        duration = self.borrow_duration.strip().lower()
        if "week" in duration:
            weeks = int(duration.split()[0])
            self.due_date = add_days(issue_date, weeks * 7)
        elif "month" in duration:
            months = int(duration.split()[0])
            self.due_date = add_months(issue_date, months)
        else:
            self.due_date = add_days(issue_date, 7)

        if not self.due_date:
            self.due_date = add_days(self.issue_date or nowdate(), 7)

    def on_submit(self):
        # Message when book is issued
        frappe.msgprint(f"Book '{self.book}' issued to member '{self.member}'. Due date: {self.due_date}")

    def on_cancel(self):
        # When the transaction is canceled or book is returned
        book = frappe.get_doc("Book", self.book)
        book.available_copies += 1
        book.save()
        self.return_date = nowdate()
        self.status = "Returned"
        self.save()

        frappe.msgprint(f"Book '{self.book}' returned successfully by member '{self.member}'.")








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
