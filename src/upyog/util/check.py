from upyog.util.eject import ejectable

@ejectable()
def check_array(o, raise_err = True):
    """
    Check if an object is array-like.

    Args:
        o (object): The object to be checked.
        raise_err (bool): If True, raises an error if the object is not an array.
    
    Returns:
        bool: True if the object is an array, False otherwise.

    Raises:
        TypeError: If the object is not an array and raise_err is True.

    Example::
        >>> check_array([1, 2, 3])
        True
        >>> check_array((1, 2, 3))
        True
        >>> check_array({1, 2, 3})
        True
        >>> check_array(1, raise_err = False)
        False
        >>> check_array("foobar")
        TypeError: Object is not an array.
    """
    if isinstance(o, (list, tuple, set)):
        return True
    else:
        if raise_err:
            raise TypeError("Object is not an array.")
        else:
            return False