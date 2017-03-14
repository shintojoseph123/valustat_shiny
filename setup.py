from setuptools import setup

setup(
   name='valustat_shiny',
   version='1.0',
   description='first version of valustat shiny app',
   author='valustat_team',
   author_email='deepak.arackal@valustat.co.uk',
   packages=['valustat_shiny'],  #same as name
   install_requires=['django==1.9.6', 'numpy==1.11.3', 'plotly==1.12.12', 'pytz==2016.10', 'requests==2.12.5', 'six==1.10.0'], #external packages as dependencies
)
