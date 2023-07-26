import abc


class Singleton(abc.ABCMeta, type):
    "Singleton metaclass for ensuring only one instance of a class."

    _instances = {}

    def __call__(self, *args, **kwargs):
        """Call method for the singleton metaclass."""
        if self not in self._instances:
            instance = super(Singleton, self).__call__(*args, **kwargs)
            self._instances[self] = instance
            self.instance = instance  # Store the instance at class level
        return self._instances[self]
