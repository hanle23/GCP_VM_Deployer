from setuptools import setup


# # Parse version number from pyglet/__init__.py:
# with open('/deployable/__init__.py') as f:
#     info = {}
#     for line in f:
#         if line.startswith('version'):
#             exec(line, info)
#             break


setup_info = dict(
    name='deployable',
    version='0.0.1',
    author='Quang Hieu Le',
    author_email='hanle.cs23@gmail.com',
    download_url='https://github.com/York-University-SCS/Deployable',
    description='Auto Deployment Tool using Google Cloud API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    py_modules=[],

    # Package info
    install_requires=[
        'google_api_python_client==2.81.0',
        'oauth2client==4.1.3',
        'requests==2.28.2',
        'setuptools==65.5.0'
    ],
    # Add _ prefix to the names of temporary build dirs
    options={'build': {'build_base': '_build'}, },
    zip_safe=True,
)

setup(**setup_info)
