from setuptools import setup, find_packages

setup(
    name='WalletWave',
    version='1.0',
    description='A CLI program to analyze top performing SOLANA wallets specifically for copy trading',
    author='LetsStartWithPurple',
    author_email='LetsStartWithPurple@gmail.com',
    packages=find_packages(),
    install_requires=[
        "PyYAML",
        "fake-useragent",
        "tls_client"
    ],
    url='https://github.com/LetsStartWithPurple/WalletWave',
    license='CC0 1.0 Universal (Public Domain Dedication)',
    classifiers=[
      "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (Public Domain Dedication)",
        "Operating System :: OS Independent"
    ],
    entry_points={
        "console_scripts": [
            "walletwave=WalletWave.main:main"
        ]
    },
    include_package_data=True,
)