frappe.ui.form.on('Library Transaction', {
    onload: function(frm) {
        // إخفاء return_date عند الإنشاء، إظهار عند عرض السجل
        if (frm.is_new()) {
            frm.set_df_property('return_date', 'hidden', 1);
        } else {
            frm.set_df_property('return_date', 'hidden', 0);
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
    if(frm.doc.issue_date && frm.doc.borrow_duration) {
        let duration = frm.doc.borrow_duration.trim().toLowerCase();
        let due_date;

        if(duration.includes("week")) {
            let weeks = parseInt(duration.split(" ")[0]);
            due_date = frappe.datetime.add_days(frm.doc.issue_date, weeks * 7);
        } else if(duration.includes("month")) {
            let months = parseInt(duration.split(" ")[0]);
            due_date = frappe.datetime.add_months(frm.doc.issue_date, months);
        } else {
            due_date = frappe.datetime.add_days(frm.doc.issue_date, 7);
        }

        frm.set_value("due_date", due_date);
    }
}
