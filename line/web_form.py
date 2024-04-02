import base64
import json
from collections.abc import Callable
import frappe
from frappe.core.doctype.file.utils import remove_file_by_url


@frappe.whitelist(allow_guest=True)
def update_profile(web_form, data):
    return accept(web_form, data)
 
def accept(web_form, data):
    """Save the web form"""
    data = frappe._dict(json.loads(data))

    files = []
    files_to_delete = []

    web_form = frappe.get_doc("Web Form", web_form)
    doctype = web_form.doc_type
    user = frappe.session.user
 
    
    if web_form.anonymous and frappe.session.user != "Guest":
        frappe.session.user = "Guest"

    if data.name and not web_form.allow_edit:
        frappe.throw(_("You are not allowed to update this Web Form Document"))

    frappe.flags.in_web_form = True
    meta = frappe.get_meta(doctype)

    if data.name:
        # update
        doc = frappe.get_doc(doctype, data.name)
    else:
        # insert
        doc = frappe.new_doc(doctype)

    # set values
    for field in web_form.web_form_fields:
        fieldname = field.fieldname
        df = meta.get_field(fieldname)
        value = data.get(fieldname, "")

        if df and df.fieldtype in ("Attach", "Attach Image"):
            if value and "data:" and "base64" in value:
                files.append((fieldname, value))
                if not doc.name:
                    doc.set(fieldname, "")
                continue

            elif not value and doc.get(fieldname):
                files_to_delete.append(doc.get(fieldname))

        doc.set(fieldname, value)


    if doc.name:
        if web_form.has_web_form_permission(doctype, doc.name, "write"):
            
            if doctype == "User":
                check_customer(doc)
            doc.save(ignore_permissions=True)
        else:
            doc.save()

    else:
        # insert
        if web_form.login_required and frappe.session.user == "Guest":
            frappe.throw(_("You must login to submit this form"))

        ignore_mandatory = True if files else False

        doc.insert(ignore_permissions=True, ignore_mandatory=ignore_mandatory)

    # add files
    if files:
        for f in files:
            fieldname, filedata = f

            # remove earlier attached file (if exists)
            if doc.get(fieldname):
                remove_file_by_url(doc.get(fieldname), doctype=doctype, name=doc.name)

            # save new file
            filename, dataurl = filedata.split(",", 1)
            _file = frappe.get_doc(
                {
                    "doctype": "File",
                    "file_name": filename,
                    "attached_to_doctype": doctype,
                    "attached_to_name": doc.name,
                    "content": dataurl,
                    "decode": True,
                }
            )
            _file.save()

            # update values
            doc.set(fieldname, _file.file_url)

        doc.save(ignore_permissions=True)

    if files_to_delete:
        for f in files_to_delete:
            if f:
                remove_file_by_url(f, doctype=doctype, name=doc.name)

    if web_form.anonymous and frappe.session.user == "Guest" and user:
        frappe.session.user = user

    frappe.flags.web_form_doc = doc
    return doc



def check_customer(doc):
    filters = {"user": "itsgoraya@gmail.com"}
    documents = frappe.get_all("Contact", filters=filters, fields=["*"])
    
    for doc in documents:
        contact = frappe.get_doc("Contact", doc.name)
        links =  contact.links
        if not links:
            customer = _create_customer(doc.first_name,doc.email_id)
            contact.append("links",{
                    "link_doctype": "Customer",
                    "link_name": customer.name,
            })
            contact.save(ignore_permissions=True) 
            frappe.publish_realtime('new_customer', {'customer_name': customer.name,'email_id': customer.email_id,'name': customer.name,'tax_id': "",'phone': ""})

def _create_customer(customer_name,email_id):
    filters = {"email_id": email_id}
    customer = frappe.get_all("Customer", filters=filters, fields=["*"])
    
    if customer:
        return customer[0]
    else:
        new_customer = frappe.new_doc('Customer')
        new_customer.customer_name = customer_name
        new_customer.territory = "Thailand"
        new_customer.phone = customer_name
        new_customer.email_id = email_id
        new_customer.insert(
            ignore_permissions=True,
            ignore_links=True,
            ignore_mandatory=True
        )
        new_customer.save()
        return new_customer