import setuptools

setuptools.setup(
    name="uti-demo-package",
    version="0.0.1",
    author="MihraceTabiloğlu",
    author_email="mihracetabiloglu@gmail.com",  
    description="UTI Demo Package Assignment",
    url="https://github.com/mihrace-saliha/uti-demo-package",
    license="MIT",
    type="capsule",
    install_requires=["sdk", "opencv-python-headless"],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    packages=[
        "novavision.package",
        "novavision.package.apps",
        "novavision.package.resources",
        "novavision.package.executors",
        "novavision.package.models",
        "novavision.package.utils"
    ],
    package_dir={"novavision.package": "src"},
    python_requires=">=3.6"
)