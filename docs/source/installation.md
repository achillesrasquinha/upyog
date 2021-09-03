### Installation

#### Installation via pip

The recommended way to install **bpyutils** is via `pip`.

```shell
$ pip install bpyutils
```

For instructions on installing python and pip see “The Hitchhiker’s Guide to Python” 
[Installation Guides](https://docs.python-guide.org/starting/installation/).

#### Building from source

`bpyutils` is actively developed on [GitHub](https://github.com/achillesrasquinha/bpyutils)
and is always avaliable.

You can clone the base repository with git as follows:

```shell
$ git clone git@github.com:achillesrasquinha/bpyutils.git
```

Optionally, you could download the tarball or zipball as follows:

##### For Linux Users

```shell
$ curl -OL https://github.com/achillesrasquinha/tarball/bpyutils
```

##### For Windows Users

```shell
$ curl -OL https://github.com/achillesrasquinha/zipball/bpyutils
```

Install necessary dependencies

```shell
$ cd bpyutils
$ pip install -r requirements.txt
```

Then, go ahead and install bpyutils in your site-packages as follows:

```shell
$ python setup.py install
```

Check to see if you’ve installed bpyutils correctly.

```python
$ python
>>> import bpyutils
```