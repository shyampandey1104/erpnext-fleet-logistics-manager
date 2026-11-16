# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "fleet"
app_title = "Erpnext Fleet Logistics Manager"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Fleet Logistics Manager for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/fleet/css/fleet.bundle.css"
app_include_js = "/assets/fleet/js/fleet.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "fleet.engine.on_document_submit",
        "on_cancel": "fleet.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "fleet.engine.daily_scheduled_sync"
    ]
}
