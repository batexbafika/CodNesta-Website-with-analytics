"""
Main Navigation Routes Blueprint
Handles static core views: Home, Services, About, and Portfolio.
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Renders the modular home page."""
    return render_template('main/index.html', title="Home")


@main_bp.route('/services')
def services():
    """Renders concise services overview."""
    return render_template('main/services.html', title="Services")


@main_bp.route('/privacy-policy')
def privacy_policy():
    """Renders the privacy policy."""
    return render_template('main/privacy-policy.html', title="Privacy Policy")


@main_bp.route('/about')
def about():
    """Renders brief company/developer details."""
    return render_template('main/about.html', title="About Us")

@main_bp.route('/ecosystem')
def ecosystem():
    """Renders the ecosystem page."""
    return render_template('main/ecosystem.html', title="Ecosystem")