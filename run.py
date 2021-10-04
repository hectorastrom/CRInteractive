from app import app, db, is_production

if __name__ == '__main__':
    db.create_all()
    if is_production:
        app.run(debug=False)
    else:
        app.run(debug=True)