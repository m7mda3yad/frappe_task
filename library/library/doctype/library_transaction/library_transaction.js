frappe.ui.form.on('Library Transaction', {
    refresh: function(frm) {
        if (frm.doc.status === "Issued" && !frm.is_new()) {
            frm.add_custom_button(__('Return Book'), function() {
                frappe.call({
                    method: "library.library.doctype.library_transaction.library_transaction.return_book",
                    args: { docname: frm.doc.name },
                    callback: function(r) {
                        if (!r.exc) {
                            frappe.msgprint(__('Book returned successfully!'));
                            frm.reload_doc();
                        }
                    }
                });
            }, __("Actions"));
        }
    },

    issue_date: function(frm) {
        calculate_due_date(frm);
    },

    borrow_duration: function(frm) {
        calculate_due_date(frm);
    }
});

function calculate_due_date(frm) {
    if (frm.doc.issue_date && frm.doc.borrow_duration) {
        let duration = frm.doc.borrow_duration.trim().toLowerCase();
        let due_date;

        if (duration.includes("week")) {
            let weeks = parseInt(duration.split(" ")[0]);
            due_date = frappe.datetime.add_days(frm.doc.issue_date, weeks * 7);
        } else if (duration.includes("month")) {
            let months = parseInt(duration.split(" ")[0]);
            due_date = frappe.datetime.add_months(frm.doc.issue_date, months);
        } else {
            due_date = frappe.datetime.add_days(frm.doc.issue_date, 7);
        }

        frm.set_value("due_date", due_date);
    }
}
