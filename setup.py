from setuptools import find_packages
from setuptools import setup

setup(
    name='streamingbot',
    version='0.0.2',
    url='http://github.com/pirxthepilot/streamingbot',
    license='MIT',
    author='Joon Guillen',
    description='Twitch live stream notifier for Slack',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'arrow',
        #'boto3~=1.12.38',
        'requests~=2.23.0',
        'simplejson',
        'twitch-python~=0.0.18',
    ]
)
