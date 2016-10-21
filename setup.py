from setuptools import setup

setup(name='i3-workspace-rollback',
      version='1.1',
      description='i3 plugin for rollback to last focused workspace',
      url='https://github.com/alexrochas/i3-workspace-rollback',
      author='Alex Rocha',
      author_email='alex.rochas@yahoo.com.br',
      license='MIT',
      packages=['rollback'],
      install_requires=['enum-compat==0.0.2',
                        'i3ipc==1.3.0',
                        'mock==2.0.0',
                        'nose==1.3.7',
                        'pbr==1.10.0',
                        'six==1.10.0'],
      entry_points={
          'console_scripts': ['i3-workspace-rollback=rollback.rollback:start'],
      },
      include_package_data=True,
      zip_safe=False)
