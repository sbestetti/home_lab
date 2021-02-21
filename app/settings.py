# Main settings
TESTING = True
SECRET_KEY = "secret"
PERMANENT_SESSION_LIFETIME = 3600
JSONIFY_PRETTYPRINT_REGULAR = True

# Google API settings
CLIENTSECRETS_LOCATION = "app/modules/client_secret.json"
REDIRECT_URI = "https://localhost:8000/oauth_redirect"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
# SCOPES = ["https://www.googleapis.com/auth/gmail.metadata"]

# SQL settings
# SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
# SQLALCHEMY_TRACK_MODIFICATIONS = False
