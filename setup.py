try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

with open('README') as file:
    long_description = file.read()

setup(name='flask-restful-swagger',
      version='0.19',
      url='https://github.com/rantav/flask-restful-swagger',
      zip_safe=False,
      packages=['flask_restful_swagger'],
      package_data={
        'flask_restful_swagger': [
          'static/*.*',
          'static/css/*.*',
          'static/images/*.*',
          'static/lib/*.*',
          'static/lib/shred/*.*',
          'templates/*.*'
        ]
      },
      description='Extrarct swagger specs from your flast-restful project',
      author='Ran Tavory',
      license='MIT',

      #dependency_links=['https://github.com/aloha1003/flask-gevent-socketio-chat'],
      dependency_links=['https://github.com/aloha1003/flask-gevent-socketio-chat','https://github.com/aloha1003/LINE'],
      long_description=long_description,
      install_requires=['Flask-RESTful>=0.2.12',"Jinja2==2.6","Werkzeug==0.8.3","gevent==0.13.8","gevent-socketio==0.3.5-rc2","gevent-websocket==0.3.6","greenlet==0.4.0","wsgiref==0.1.2"]
      )
