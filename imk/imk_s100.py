from dotenv import load_dotenv
from functools import cached_property

from imk.imk_collections import ImkCollections
from imk.imk_gpt import ImkGpt
from imk.imk_io import ImkIo

load_dotenv()


class ImkPythonS100:
    def __init__(self, s100):
        self.s100 = s100

    @cached_property
    def coll(self) -> ImkCollections: return ImkCollections()

    @cached_property
    def io(self) -> ImkIo: return ImkIo(self.s100)

    @cached_property
    def gpt(self) -> ImkGpt: return ImkGpt(self.s100)


class ImkS100:
    @property
    def py(self) -> ImkPythonS100:
        return ImkPythonS100(self)


s100 = ImkS100()
