class LoxReturn(RuntimeError):
    def __init__(self, value: object):
        super()
        self.value = value
