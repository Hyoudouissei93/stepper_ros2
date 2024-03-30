from setuptools import find_packages, setup

package_name = 'my_stepper'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yourkeeriew',
    maintainer_email='yourkeeriew@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pub_stepper = my_stepper.stepper_talker:main',
            'sub_stepper = my_stepper.stepper_listener:main'
        ],
    },
)
