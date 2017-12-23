from setuptools import setup, find_packages

setup(
    name='s3wrap',
    author='Jacob Feala',
    author_email='jake@outlierbio.com',
    version='0.1',
    url='http://github.com/outlierbio/s3wrap',
    packages=find_packages(),
    description='Use S3 URIs as arguments for any command-line tool',
    include_package_data=True,
    install_requires=[
        'boto3',
        'click'
    ],
    entry_points='''
        [console_scripts]
        s3wrap=s3wrap.s3:s3wrap
    '''
)