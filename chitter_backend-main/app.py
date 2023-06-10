# pipenv shell
# flask db upgrade
# flask seed all
# flask run




from application import app
from application import socketIo

if __name__ == '__main__':
    app.run(debug=True)