from apptrak import create_app, csrf


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
