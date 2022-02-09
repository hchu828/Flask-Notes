from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    """Form to register a new user"""

    username = StringField(
        "Username", validators=[InputRequired(), Length(max=20)]
    )  # TODO: length(max)

    password = PasswordField(
        "Password", validators=[InputRequired(), Length(max=100)]
    )

    email = EmailField("Email", validators=[InputRequired(), Length(max=50)])

    first_name = StringField(
        "First Name", validators=[InputRequired(), Length(max=30)]
    )

    last_name = StringField(
        "Last Name", validators=[InputRequired(), Length(max=30)]
    )


class LoginForm(FlaskForm):
    """Form to login a user"""

    username = StringField(
        "Username", validators=[InputRequired(), Length(max=30)]
    )

    password = PasswordField(
        "Password", validators=[InputRequired(), Length(max=30)]
    )


class AddNoteForm(FlaskForm):
    """Form for adding a new note"""

    title = StringField(
        "Title",
        validators=[
            InputRequired(),
            Length(max=100),
        ],
    )
    content = StringField("Content", validators=[InputRequired()])


class CSRFProtectForm(FlaskForm):
    """Form used for CSRF protection."""
