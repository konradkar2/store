from flask_jwt_extended import JWTManager
from flask import jsonify

def set_jwt_settings(jwt: JWTManager):
    @jwt.expired_token_loader
    def expired_token_callback():
        return jsonify({
            'description': 'The token has expired',
            'error': 'expired_token'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'description': 'Signature verification failed',
            'error': 'invalid_token'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'description': 'Request does not contain access token',
            'error': 'authorization_required'
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback():
        return jsonify({
            'description': 'The token has been revoked',
            'error': 'revoked_token'
        }), 401
