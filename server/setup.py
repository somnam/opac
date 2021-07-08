from setuptools import setup

install_requires = [
    "aiohttp==3.7.4",
    "beautifulsoup4==4.9.3",
    "lxml==4.6.3",
    "tornado==6.1",
    "jsonschema==3.2.0",
    "requests==2.25.1",
    "redis==3.5.3",
    "rq==1.9.0",
]

setup_requires = [
    "pytest-runner",
]

tests_require = [
    "mypy<0.900",
    "pytest-flake8",
    "pytest-mypy",
]

extras_require = {
    "dev": [
        "autopep8",
        "flake8",
        *tests_require,
    ],
}

entry_points = {
    "console_scripts": [
        "run_app=src.entrypoints.websocket.app:run",
        "run_worker=src.entrypoints.jobs.worker:run",
    ],
}

setup(
    name="opac",
    version="0.0.1",
    description="opac app",
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    entry_points=entry_points,
)
