class Empty(Exception):
    """
    Exception when attempting to access an element from an empty container.
    """
    pass


class Full(Exception):
    """
    Exception when attempting to add an element to a full container.
    """
    pass
