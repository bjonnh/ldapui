from app import db


class ResetCodes(db.Model):
    """Model used to store the password reset codes"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256))
    email = db.Column(db.String(256))
    code = db.Column(db.String(64))
