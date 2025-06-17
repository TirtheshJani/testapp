from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from . import bp  # Fixed: import from current module

@bp.route('/login')
def login():
    """Display login page with OAuth options."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """Log out the current user."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

# OAuth routes will be added later
@bp.route('/login/<provider>')
def oauth_login(provider):
    """Placeholder for OAuth login."""
    flash(f'OAuth login with {provider} not yet configured.', 'warning')
    return redirect(url_for('auth.login'))