from setuptools import find_packages
from setuptools import setup

setup(
    name='streamingbot',
    version='0.1.0',
    url='http://github.com/pirxthepilot/streamingbot',
    license='MIT',
    author='pirxthepilot',
    description='Twitch live stream notifier for Slack',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'arrow',
        'requests~=2.31.0',
        'simplejson',
        'twitchAPI~=4.1.0',
    ]
)
