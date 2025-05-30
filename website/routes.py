from .rendering import render, render_404
from .logic.auth import (login as login_handler, google_auth, apple_auth, microsoft_auth,
                         signup as signup_handler, confirm as confirm_handler, reset as reset_handler)
from .logic.auth.verification import empty_token, is_admin
from .logic.blog import preview as blog_preview, create as blog_creator, post as blog_post_handler
from .logic import index as index_handler
from flask import Blueprint, redirect, flash
from LIBRARY import ALL_METHODS

routes = Blueprint('routes', __name__)
auth_routes = Blueprint('auth_routes', __name__)


# Main Routes
@routes.route('/')
def index():
    return index_handler.handle_request()


# Blog routes
@routes.route('/blog')
def blog():
    return blog_preview.handle_request()


@routes.route('/blog/<blog_id>')
def blog_post(blog_id):
    return blog_post_handler.handle_request(blog_id)


@routes.route('/blog/new', methods=ALL_METHODS)
def new_blog_post():
    if not is_admin():
        flash("Du bist leider nicht für das Erstellen von Blogeinträgen berechtigt.", 'danger')
        return redirect('/blog')

    return blog_creator.handle_request()


# Authentication routes
@auth_routes.route('/login', methods=ALL_METHODS)
def login():
    return login_handler.handle_request()


@auth_routes.route('/signup', methods=ALL_METHODS)
def signup():
    return signup_handler.handle_request()


@auth_routes.route('/notice/confirm/<code>')
def confirm_notice(code):
    return confirm_handler.confirm_notice(code)


@auth_routes.route('/confirm/<code>')
def confirm(code):
    return confirm_handler.handle_confirm(code)


@auth_routes.route('/reset/<code>', methods=ALL_METHODS)
def reset(code):
    return reset_handler.handle_request(code)


@auth_routes.route('/logout')
def logout():
    return empty_token()


@auth_routes.route('/oauth/<api>/start')
def start_oauth(api):
    return google_auth.start_oauth() if api == 'google' else (
        apple_auth.start_oauth() if api == 'apple' else (
            microsoft_auth.start_oauth() if api == 'microsoft' else render_404()
        )
    )


@routes.route('/oauth/<api>/callback', methods=ALL_METHODS)
def oauth_callback(api):
    return google_auth.oauth_callback() if api == 'google' else (
        apple_auth.oauth_callback() if api == 'apple' else (
            microsoft_auth.oauth_callback() if api == 'microsoft' else render_404()
        )
    )


# Legal Routes
@routes.route('/about')
def about():
    return render("site/about.html")


@routes.route('/privacy')
def privacy():
    return render("site/privacy.html")


@routes.route('/guidelines')
def guidelines():
    return render("site/guidelines.html")


@routes.route('/impressum')
def impressum():
    return render("site/impressum.html")


# Not Found
@routes.route('/<path:path>')
def not_found(path):
    return render_404()


# Processing debug requests for testing
@routes.route('/debug')
def debug():
    """

        TODO: Debug Stuff

    """
    return redirect('/')