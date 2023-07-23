import frappe

def before_uninstall():
    if frappe.db.exists("Social Login Key", "line"):
        frappe.delete_doc("Social Login Key", "line")