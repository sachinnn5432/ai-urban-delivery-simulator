# This is a shim to fix compatibility issues with VPython on newer Python versions
def get_distribution(package_name):
    class DummyDistribution:
        version = "7.6.5"
    return DummyDistribution()

class DistributionNotFound(Exception):
    pass
