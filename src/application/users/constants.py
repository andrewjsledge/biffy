__author__ = 'andrew'

# User role
ADMIN = 0
STAFF = 1
USER = 2
ROLE = {
    ADMIN: 'Admin',
    STAFF: 'Staff',
    USER: 'User',
}

# user status
INACTIVE = 0
NEW = 1
ACTIVE = 2
STATUS = {
    INACTIVE: 'Inactive',
    NEW: 'New',
    ACTIVE: 'Active',
}

# auth services
LOCAL = 0
TWITTER = 1
GOOGLE = 2
FACEBOOK = 3
AUTH_SERVICE = {
    LOCAL: 'Local',
    TWITTER: 'Twitter',
    GOOGLE: 'Google',
    FACEBOOK: 'Facebook',
}

# static messaging
ALREADY_LOGGED_IN = u'You are already logged in!'
ALREADY_ASSOCIATED = u'Your %s ID %s is already associated with your account.'
ASSOCIATION_COMPLETE = u'Your %s ID %s has been associated with your account.'
ACCESS_REQUIRED = u'You must have admin permissions to access this area.'
LOGIN_REQUIRED = u'You must log in to access this area.'
LOGIN_DENIED = u'You were denied the request to sign in.'
DENIED_MULTIPLE_ACCOUNTS = u'As a non-member, you cannot log in with multiple' \
                           u' accounts.'
REGISTRATION_SUCCESSFUL = u'Thanks for registering!'
PROFILE_UPDATE_SUCCESSFUL = u'Your profile has been successfully updated.'
PROFILE_UPDATE_FAILED = u'There was a problem in saving your profile.'