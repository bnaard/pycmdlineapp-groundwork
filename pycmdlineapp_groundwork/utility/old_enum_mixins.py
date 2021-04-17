

# mixin code from https://github.com/PyCQA/pylint/issues/533 

class IntStrEnumMixin:
    def __new__(cls, value, description):
        member = object.__new__(cls)
        member._value_ = value
        member._description = description
        return member

    @property
    def description(self):
        return self._desc

    def __int__(self):
        return self.value

    def __str__(self):
        return self.description
