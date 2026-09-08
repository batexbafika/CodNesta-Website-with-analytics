import math
import re
from flask import Blueprint, current_app, jsonify, render_template, request
from flask_limiter import RateLimitExceeded
from flask_mail import Message

# Import instances directly from app module
from app import db, mail, limiter
from app.models.contact import ContactMessage

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
    retry_after_seconds = getattr(e, "retry_after", 3600)
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