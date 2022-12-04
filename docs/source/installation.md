### Installation

#### Installation via pip

The recommended way to install **upyog** is via `pip`.

```shell
$ pip install upyog
```

For instructions on installing python and pip see “The Hitchhiker’s Guide to Python” 
[Installation Guides](https://docs.python-guide.org/starting/installation/).

#### Building from source

`upyog` is actively developed on [GitHub](https://github.com/achillesrasquinha/upyog)
and is always avaliable.

You can clone the base repository with git as follows:

```shell
$ git clone git@github.com:achillesrasquinha/upyog.git
```

Optionally, you could download the tarball or zipball as follows:

##### For Linux Users

```shell
$ curl -OL https://github.com/achillesrasquinha/tarball/upyog
```

##### For Windows Users

```shell
$ curl -OL https://github.com/achillesrasquinha/zipball/upyog
```

Install necessary dependencies

```shell
$ cd upyog
$ pip install -r requirements.txt
```

Then, go ahead and install upyog in your site-packages as follows:

```shell
$ python setup.py install
```

Check to see if you’ve installed upyog correctly.

```python
$ python
>>> import upyog
```