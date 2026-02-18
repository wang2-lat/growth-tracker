from setuptools import setup, find_packages

setup(
    name="growth-tracker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer==0.12.3",
        "rich==13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "growth=growth_tracker.cli:app",
        ],
    },
)