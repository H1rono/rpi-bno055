from setuptools import setup

package_name = "rpi_bno055"

setup(
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
    ]
)
