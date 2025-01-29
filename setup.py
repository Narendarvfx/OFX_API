from setuptools import setup

setup(
    name='ofx_api',
    version='V003',
    packages=['hrm', 'hrm.migrations', 'essl', 'wsapi', 'wsdoc', 'history', 'history.migrations', 'OFX_API', 'profiles',
              'ofx_common', 'ofx_common.templatetags', 'production', 'production.migrations', 'websockets',
              'pipeline_api', 'pipeline_api.migrations', 'dynamicfilters', 'ofx_dashboards', 'ofx_statistics',
              'ofx_statistics.migrations', 'shotassignments', 'time_management', 'wsnotifications'],
    url='https://shotbuzz.oscarfx.com',
    license='OSCARFX',
    author='NARENDAR REDDY G',
    author_email='',
    description=''
)
