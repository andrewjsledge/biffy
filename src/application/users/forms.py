from flask.ext.wtf import Form, TextField, PasswordField, BooleanField, RecaptchaField
from flask.ext.wtf import Required, Email, EqualTo, ValidationError
from application.utils import is_us_phone_number

class EmailLoginForm(Form):
    email = TextField('Email', [Required(), Email()])
    password = PasswordField('Password', [Required()])

class RegisterForm(Form):
    first_name = TextField('First Name', validators=[Required()],
        description="Your first name")
    last_name = TextField('Last Name', validators=[Required()],
        description="Your last name")
    email = TextField('Email address', validators=[Required(), Email()],
        description="Your email address")
    phone = TextField('Phone number', validators=[Required()],
        description="Your phone number")
    password = PasswordField('Password',
        validators=[Required(), EqualTo('confirm', message='Passwords must match')],
        description="Your password")
    confirm = PasswordField('', validators=[Required()],
        description="Confirm your password")

    def validate_phone(form, field):
        if not is_us_phone_number(field.data):
            raise ValidationError('Use the phone number format XXX-XXX-XXXX')


class ProfileForm(RegisterForm):
    first_name = TextField('First Name', validators=[Required()],
        description="Your first name")
    last_name = TextField('Last Name', validators=[Required()],
        description="Your last name")
    email = TextField('Email address', validators=[Required(), Email()],
        description="Your email address")
    phone = TextField('Phone number', validators=[Required()],
        description="Your phone number")

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        del self.confirm
        del self.password