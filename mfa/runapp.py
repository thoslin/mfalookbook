if __name__ == "__main__":
    from mfa.lookbook.app import app
    from mfa.lookbook.models import init_db
    init_db()
    app.run(debug=True, host="0.0.0.0")