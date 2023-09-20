class InitializeKwargsMixin:
    """
    Класс mixin, для инициализции дополнительных аттрибутов в объектах модели
    """

    def initialize_kwargs(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
