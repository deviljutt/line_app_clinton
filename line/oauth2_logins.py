import json

import frappe
from frappe.utils.oauth import login_oauth_user,login_via_oauth2,login_via_oauth2_id_token

@frappe.whitelist(allow_guest=True)
def login_via_line(code: str, state: str):
	login_via_oauth2_id_token("line", code, state, decoder=decoder_compat)
	# login_via_oauth2("line", code, state, decoder=decoder_compat)
	# info = get_info_via_oauth(provider, code, decoder)
	# login_oauth_user(info, provider=provider, state=state)

# def get_info_via_oauth(
# 	provider: str, code: str, decoder: Callable | None = None, id_token: bool = False
# ):
# 	flow = get_oauth2_flow(provider)
# 	oauth2_providers = get_oauth2_providers()

# 	args = {
# 		"data": {
# 			"code": code,
# 			"redirect_uri": get_redirect_uri(provider),
# 			"grant_type": "authorization_code",
# 		}
# 	}

# 	if decoder:
# 		args["decoder"] = decoder

# 	print("args =>", args)
# 	print("flow =>", flow.__dict__)
# 	session = flow.get_auth_session(**args)
# 	print("session =>", json.loads(session.access_token_response.text))
# 	if id_token:
# 		parsed_access = json.loads(session.access_token_response.text)
# 		token = parsed_access["id_token"]
# 		info = jwt.decode(token, flow.client_secret, options={"verify_signature": False})

# 	else:
# 		api_endpoint = oauth2_providers[provider].get("api_endpoint")
# 		api_endpoint_args = oauth2_providers[provider].get("api_endpoint_args")
# 		info = session.get(api_endpoint, params=api_endpoint_args).json()

# 		if provider == "github" and not info.get("email"):
# 			emails = session.get("/user/emails", params=api_endpoint_args).json()
# 			email_dict = list(filter(lambda x: x.get("primary"), emails))[0]
# 			info["email"] = email_dict.get("email")

# 	print("info =>", info)
# 	if not (info.get("email_verified") or info.get("email")):
# 		frappe.throw(_("Email not verified with {0}").format(provider.title()))

# 	return info
	
def decoder_compat(b):
	# https://github.com/litl/rauth/issues/145#issuecomment-31199471
	return json.loads(bytes(b).decode("utf-8"))