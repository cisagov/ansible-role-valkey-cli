"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_packages(host):
    """Test that the appropriate packages were installed."""
    distribution = host.system_info.distribution
    pkgs = None
    if distribution in ["debian", "kali", "ubuntu"]:
        pkgs = ["valkey-tools"]
    elif distribution in ["amzn", "fedora"]:
        pkgs = ["valkey"]
    else:
        # This is an unknown OS, so force the test to fail
        assert False, f"Unknown distribution {distribution}"

    for pkg in pkgs:
        assert host.package(pkg).is_installed, f"Package {pkg} is not installed."
