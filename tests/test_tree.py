from src.mcfg_parser_aditya_dan.tree import *


class TestTree:

    test_object = Tree('S', ((0, 5,),))

    def test_object_creation(self):
        assert isinstance(self.test_object, Tree)

    def test_add_child(self):
        self.test_object.add_child(Tree('NP', ((0, 1,),)))
        assert self.test_object.is_leaf() is False
