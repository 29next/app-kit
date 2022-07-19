<!-- Badges -->
[![PyPI Version][pypi-v-image]][pypi-v-link]
[![Build Status][GHAction-image]][GHAction-link]
[![CodeCov][codecov-image]][codecov-link]

# 29 Next App Kit

App Kit is a cross-platform command line tool to build and maintain apps on the 29 Next platform.

## Installation

App Kit is a python package available on [PyPi](https://pypi.org/project/next-app-kit/)

If you already have `python` and `pip`, install with the following command:

```
pip install next-app-kit
```

#### Mac OSX Requirements
See how to install `python` and `pip` with [HomeBrew](https://docs.brew.sh/Homebrew-and-Python#python-3x). Once you have completed this step you can install using the `pip` instructions above.

#### Windows Requirements
See how to install `python` and `pip` with [Chocolatey](https://python-docs.readthedocs.io/en/latest/starting/install3/win.html). Once you have completed this step you can install using the `pip` instructions above.


#### Updating App Kit

Update to the latest version of App Kit with the following command:
```
pip install next-app-kit --upgrade
```

> :warning: **Important**
>
> Usage requires a Partner Account and an App Client ID, create and setup your partner account [here](https://accounts.29next.com/partners/).

## Usage
With the package installed, you can now use the commands inside your app directory to build and push your app updates.

**Available Commands**
* `nak setup` - configure current directory with an app in your account
* `nak build` - build new app zip file
* `nak push` - push latest app zip file to 29 Next platform


#### Setup
Configures the current directory with necessary data to push the app files to 29 Next.

**Data collected by the `setup` command:**
* **App Client ID** - retrieve this from the app in your partner account.
* **Email** - your email used to access your partner account.
* **Password** - your password used to access your partner account.

#### Build
Creates a new version (zip of the current directory files) to prepare your app to be pushed to 29 Next.

#### Push
Pushes the latest version to 29 Next and to your development stores to review and test your app.


[codecov-image]: https://codecov.io/gh/29next/app-kit/branch/master/graph/badge.svg?token=1QLTNSH72Y
[codecov-link]: https://codecov.io/gh/29next/app-kit

[pypi-v-image]: https://img.shields.io/pypi/v/next-app-kit.svg
[pypi-v-link]: https://pypi.org/project/next-app-kit/
[GHAction-image]: https://github.com/29next/app-kit/actions/workflows/test.yml/badge.svg?branch=master
[GHAction-link]: https://github.com/29next/app-kit/actions?query=event%3Apush+branch%3Amaster
