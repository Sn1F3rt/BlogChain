# BlogChain - A Decentralized Blogging Platform

[![License](https://img.shields.io/github/license/Sn1F3rt/BlogChain)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/Sn1F3rt/BlogChain)](/)
[![GitHub issues](https://img.shields.io/github/issues/Sn1F3rt/BlogChain)](/)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Sn1F3rt/BlogChain)](/)

## Table of Contents

- [About](#about)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running](#running)
  - [Development](#development)
  - [Production](#production)
- [License](#license)

## About

BlogChain is a decentralized blogging platform built on the Ethereum blockchain. It is the first of its kind to implement the [Sign-In with Ethereum](https://login.xyz/) authentication protocol, natively in Python using the [siwe-py](https://pypi.org/project/siwe/) library. On the core, it is built using the [Flask](https://flask.palletsprojects.com/) web framework. Database management is done using [SQLAlchemy](https://www.sqlalchemy.org/). 

It supports Ethereum based user authentication, setting username, creating and updating blog posts, and viewing blog posts. On top of that, it supports tipping post authors in order to incentivize blogging.

## Prerequisites

- Git
- Python 3.8 or higher (tested on 3.11)
- MariaDB/MySQL database
- [Ganache](https://www.trufflesuite.com/ganache) or any other Ethereum testnet

## Installation

1. Clone the repository

   ```shell
    git clone https://github.com/Sn1F3rt/BlogChain.git
   ```
   
2. Switch to the project directory

   ```shell
    cd BlogChain
   ```
   
3. Create a virtual environment

   ```shell
    python -m venv .venv
   ```
   
4. Activate the virtual environment

   ```shell
    source .venv/bin/activate
   ```
   
5. Install the dependencies

   ```shell
    pip install -r requirements.txt
   ```

## Configuration

Copy the `config.example.py` file to `config.py` and:

- update the `SECRET_KEY` variable with a 32-bit hexadecimal string.
- update the `DB_*` variables with your database credentials.
- update the `WEB3_PROVIDER` variable with the URL of your Ethereum node.

## Running

### Development

```shell
python launcher.py
```

### Production

```shell
gunicorn launcher:app
```

## License

[GNU General Public License v3.0](LICENSE)

Copyright &copy; 2024 Sayan "Sn1F3rt" Bhattacharyya
