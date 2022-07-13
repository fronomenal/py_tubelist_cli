from setuptools import setup

setup(
   name='ytlist',
   version='1.4-rc',
   description='cli for managing youtube playlists',
   author='fronomenal',
   author_email='fronomenal@gmail.com',
   url="https://github.com/fronomenal/py_tubelist_cli",
   install_requires=['google-api-python-client', 'typer', 'python-dotenv'],
)