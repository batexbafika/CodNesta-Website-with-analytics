import io
import pandas as pd
from app.extensions import db
from app.models.contact import ContactMessage

def get_contact_messages_list():
    """Returns all contact messages formatted for UI rendering."""
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return [
        {
            "id": msg.id,
            "full_name": msg.full_name,
            "email": msg.email,
            "subject": msg.subject,
            "message": msg.message,
            "ip_address": msg.ip_address or "N/A",
            "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "is_read": msg.is_read
        }
        for msg in messages
    ]

def get_contact_messages_dataframe():
    """Queries all contact messages and returns a pandas DataFrame."""
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    data = [
        {
            "ID": msg.id,
            "Full Name": msg.full_name,
            "Email": msg.email,
            "Subject": msg.subject,
            "Message": msg.message,
            "IP Address": msg.ip_address,
            "Created At": msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Is Read": msg.is_read
        }
        for msg in messages
    ]
    return pd.DataFrame(data)

def generate_csv_bytes():
    df = get_contact_messages_dataframe()
    return df.to_csv(index=False).encode("utf-8")

def generate_excel_bytes():
    df = get_contact_messages_dataframe()
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Contact Messages")
    output.seek(0)
    return output.getvalue()

def purge_all_contact_messages():
    """Deletes all records from the contact_messages table."""
    num_deleted = db.session.query(ContactMessage).delete()
    db.session.commit()
    return num_deleted