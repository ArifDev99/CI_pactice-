from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="frappe_app_example",
    version="0.0.1",
    description="Example Frappe app for CI/CD learning",
    author="CI/CD Learner",
    author_email="learner@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
) 
