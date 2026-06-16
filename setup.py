from setuptools import setup, find_packages

setup(
    name="agentbreaker-core",
    version="1.0.0",
    description="Sub-millisecond cryptographic safety shim to prevent cascading autonomous AI agent loops.",
    author="Mahima Saigal",
    author_index="mahima.saigal@gmail.com",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "httpx>=0.24.0",
        "anthropic>=0.3.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Business Source License 1.1",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
