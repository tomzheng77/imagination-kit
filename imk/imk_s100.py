class ImkPythonS100:
    def __init__(self, s100):
        self.s100 = s100


class ImkS100:
    @property
    def py(self) -> ImkPythonS100:
        return ImkPythonS100(self)


s100 = ImkS100()
