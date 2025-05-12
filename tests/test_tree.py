from src.mcfg_parser_aditya_dan.tree import *


class TestTree:

    test_object = Tree('S', ((0, 5,),))

    def test_object_creation(self):
        assert isinstance(self.test_object, Tree)

    def test_add_child(self):
        self.test_object.add_child(Tree('NP', ((0, 1,),)))
        assert self.test_object.is_leaf() is False

    def test_yield_string(self):
        assert self.test_object.yield_string(['who', 'does', 'the', 'greyhound', 'believe']) is not None

    def test_str(self):
        assert self.test_object.__str__() == "(S:((0, 5),) NP:((0, 1),))"

    def test_repr(self):
        assert self.test_object.__repr__() == "Tree('S', spans=((0, 5),), children=[Tree('NP', spans=((0, 1),), children=[])])"

