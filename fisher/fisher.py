from app import create_app

__author__ = '杨先森'

app = create_app()


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=app.config['DEBUG'])
    app.run(debug=app.config['DEBUG'], port=8000)