from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User, UserStatus
from .forms import LoginForm, RegistrationForm
from . import bp  # Fixed: import from current module

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Simple username/email and password login."""

    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.username_or_email.data
        user = (
            User.query.filter(
                (User.username == identifier) | (User.email == identifier)
            ).first()
        )
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Invalid username/email or password.', 'danger')

    return render_template('auth/login.html', form=form)

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


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            status=UserStatus.ACTIVE,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
