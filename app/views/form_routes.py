import math
import re
from io import BytesIO

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_limiter import RateLimitExceeded
from flask_mail import Message

from app import db, limiter, mail
from app.models.contact import ContactMessage
from app.services.export_service import (
    generate_csv_bytes,
    generate_excel_bytes,
    get_contact_messages_list,
    purge_all_contact_messages,
)

form_bp = Blueprint("forms", __name__)

EMAIL_REGEX = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

INQUIRY_LABELS = {
    "software_consulting": "Enterprise Software & Advisory",
    "predev_academy": "Apply for Pre-Dev Pathway",
    "intern_advance": "Intern in Advance Entry",
    "skill_programs": "Skill Bootcamps & Programs",
    "Academic_Internships": "Academic Internships",
    "Academic_Partnerships": "Academic Partnerships",
    "collective_gig": "Participating in Collective Gigs",
    "need_website": "I Need a Website",
    "need_mobile_app": "I Need a Mobile App",
    "certified_developer": "Certified Developer Program",
    "hire_developers": "Hire Verified Talent",
    "start_partnership": "Start a Partnership",
    "collaboration_request": "Project Collaboration",
    "Volunteer_with_CodNesta": "Volunteer with CodNesta",
    "agentee_business": "Joining Agentee Business Network",
    "mentorship_program": "Mentorship & Community Leadership",
    "send_feedback": "Send Us Feedback",
    "general_inquiry": "Others / General Inquiry",
}


@form_bp.errorhandler(RateLimitExceeded)
def handle_rate_limit_exceeded(e):
    retry_after_seconds = getattr(e, "retry_after", None)
    if retry_after_seconds is None:
        retry_after_seconds = 3600

    minutes_left = max(1, math.ceil(retry_after_seconds / 60))
    unit_str = "minute" if minutes_left == 1 else "minutes"

    return (
        jsonify(
            {
                "success": False,
                "error": f"You can only submit an inquiry once per hour. Please try again after {minutes_left} {unit_str}.",
            }
        ),
        429,
    )


@form_bp.route("/contact/submit", methods=["POST"])
@limiter.limit("1 per hour")
def submit_contact():
    data = request.get_json() or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    inquiry_type = data.get("inquiry_type", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not inquiry_type or not message:
        return jsonify({"success": False, "error": "All fields are required."}), 400

    if not re.match(EMAIL_REGEX, email):
        return jsonify(
            {"success": False, "error": "Invalid email address provided."}
        ), 400

    inquiry_label = INQUIRY_LABELS.get(inquiry_type, inquiry_type)

    try:
        # Store in DB
        new_contact = ContactMessage(
            full_name=name,
            email=email,
            subject=inquiry_label,
            message=message,
            ip_address=request.remote_addr,
        )
        db.session.add(new_contact)
        db.session.commit()

        # Admin Notification Email
        admin_msg = Message(
            subject=f"[CodNesta Contact] {inquiry_label} - {name}",
            recipients=[current_app.config["ADMIN_EMAIL"]],
            html=render_template(
                "emails/admin_notification.html",
                name=name,
                email=email,
                inquiry_label=inquiry_label,
                message=message,
            ),
        )
        mail.send(admin_msg)

        # User Confirmation Email
        user_msg = Message(
            subject="We received your message - CodNesta",
            recipients=[email],
            html=render_template(
                "emails/user_confirmation.html",
                name=name,
                inquiry_label=inquiry_label,
            ),
        )
        mail.send(user_msg)

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Thank you! Your message has been sent successfully.",
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"FAILED TO PROCESS CONTACT SUBMISSION: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": "A server error occurred while processing your message. Please try again later.",
                }
            ),
            500,
        )


def verify_admin_token():
    """Validates secret key token from URL parameters or form submissions."""
    token = request.args.get("token") or request.form.get("token")
    expected_token = current_app.config.get("ADMIN_EXPORT_KEY")
    if not token or token != expected_token:
        abort(403)
    return token


@form_bp.route("/admin/export-dashboard", methods=["GET"])
def admin_export_dashboard():
    token = verify_admin_token()
    messages = get_contact_messages_list()
    return render_template(
        "admin/export_dashboard.html", messages=messages, token=token
    )


@form_bp.route("/export/contact-messages/csv", methods=["GET"])
def export_contact_csv():
    verify_admin_token()
    csv_data = generate_csv_bytes()
    return send_file(
        BytesIO(csv_data),
        mimetype="text/csv",
        as_attachment=True,
        download_name="contact_messages_backup.csv",
    )


@form_bp.route("/export/contact-messages/excel", methods=["GET"])
def export_contact_excel():
    verify_admin_token()
    excel_data = generate_excel_bytes()
    return send_file(
        BytesIO(excel_data),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="contact_messages_backup.xlsx",
    )


@form_bp.route("/admin/purge-contact-messages", methods=["POST"])
def purge_contact_messages_route():
    token = verify_admin_token()
    deleted_count = purge_all_contact_messages()
    flash(
        f"Successfully purged {deleted_count} messages from the database.",
        "success",
    )
    return redirect(url_for("forms.admin_export_dashboard", token=token))