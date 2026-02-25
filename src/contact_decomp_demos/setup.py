from setuptools import find_packages, setup
import os
from glob import glob

package_name = "contact_decomp_demos"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*")),
        *[
            (os.path.join("share", package_name, os.path.dirname(f)), [f])
            for f in glob("config/**", recursive=True)
            if os.path.isfile(f)
        ],
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="David Alexander",
    maintainer_email="dmalexa5@ncsu.edu",
    description="Control a robot with the contact_decomp_controller",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "target_publisher = contact_decomp_demos.target_publisher:main",
            "crisp_py_franka_hand_adapter = contact_decomp_demos.crisp_py_franka_hand_adapter:main",
        ],
    },
)
