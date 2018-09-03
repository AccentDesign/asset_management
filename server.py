import bjoern

from app.wsgi import application


if __name__ == '__main__':
    print('Starting bjoern on port 8000...', flush=True)
    bjoern.run(application, '0.0.0.0', 8000)
