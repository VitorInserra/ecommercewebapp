from website import create_app, create_database

#run webserver:
app = create_app()

#run in debug mode:
if __name__ == '__main__':
        app.run(debug=True)