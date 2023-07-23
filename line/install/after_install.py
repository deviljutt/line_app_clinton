import json
import frappe

def after_install():
    # insert if not exists
    if not frappe.db.exists("Social Login Key", "line"):
        frappe.get_doc({
        "doctype": "Social Login Key",
        "enable_social_login": 0,
        "name": "line",
        "provider_name": "Line",
        "social_login_provider": "Custom",
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "base_url": "",
        "custom_base_url": 0,
        "authorize_url": "https://access.line.me/oauth2/v2.1/authorize",
        "access_token_url": "https://api.line.me/oauth2/v2.1/token",
        "api_endpoint": "https://api.line.me/v2/profile",
        "redirect_url": "/api/method/frappe.www.login.login_via_line/",
        "auth_url_data": json.dumps(
            {"response_type": "code", "scope": "openid profile email", "client_id": "YOUR_CLIENT_ID"}
        ),
        "api_endpoint_args": None,
    }).insert(ignore_permissions=True)  
