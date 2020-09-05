from setuptools import setup

install_requires = [
    "aiohttp",
    "beautifulsoup4",
    "lxml",
    "tornado",
    "jsonschema",
]

setup_requires = [
    'pytest-runner',
]

tests_require = [
    'pytest-flake8',
    'pytest-mypy',
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
        "run_app=entry.websocket.app:run",
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
