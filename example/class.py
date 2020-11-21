"""
# Class files

This file is an example as how your code should be done with classes.
"""


class MyClassExample:
    """
    This class shows how to start your markdowns.
    My class with a simple example of how to documentation your classes

    Args:
        `count`: int
    """

    def __init__(self, count=0):
        """
        Class constructor

        Args:
            `count`: int
        """

        self.count = count

    def get_count(self):
        """This method is used to get count's current value

        Returns:
            int: current value of count
        """

        return self.count
