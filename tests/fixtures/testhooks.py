def pytest_addoption(parser):
    parser.addoption("--start_from_jenkins",
                     action='store',
                     default=False,
                     help="True - runs from Jenkins pipeline inside docker, False - runs locally")
