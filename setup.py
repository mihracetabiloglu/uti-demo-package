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
        "novavision.uti-demo-package",
        "novavision.uti-demo-package.apps",
        "novavision.uti-demo-package.resources",
        "novavision.uti-demo-package.executors",
        "novavision.uti-demo-package.models",
        "novavision.uti-demo-package.utils"
    ],
    package_dir={"novavision.uti-demo-package": "src"},
    python_requires=">=3.6"
)