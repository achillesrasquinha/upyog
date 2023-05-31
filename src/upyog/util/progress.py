def progress(*args, **kwargs):
    """
        Returns a progress bar iterator.
    """
    try:
        from tqdm.auto import tqdm
        return tqdm(*args, **kwargs)
    except ImportError:
        raise ImportError("tqdm is required for progress bars")