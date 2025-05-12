from src.mcfg_parser_aditya_dan.grammar import *


class TestMCFGRuleElement:
    test_object = MCFGRuleElement('S', (0,), (2,))

    def test_object_creation(self):
        assert isinstance(self.test_object, MCFGRuleElement)

    def test_to_tuple(self):
        assert self.test_object.to_tuple() == ('S', ((0,), (2,)))

    def test_variable(self):
        assert self.test_object.variable == 'S'

    def test_string_variables(self):
        assert self.test_object.string_variables == ((0,), (2,),)

    def test_unique_string_variables(self):
        assert self.test_object.unique_string_variables == {0, 2}


class TestMCFGRuleElementInstance:
    test_object = MCFGRuleElementInstance('S', (0,), (2,))

    def test_object_creation(self):
        assert isinstance(self.test_object, MCFGRuleElementInstance)

    def test_to_tuple(self):
        assert self.test_object.to_tuple() == ('S', ((0,), (2,)))

    def test_variable(self):
        assert self.test_object.variable == 'S'

    def test_string_spans(self):
        assert self.test_object.string_spans == ((0,), (2,))


class TestMCFGRule:
    test_object = MCFGRule(MCFGRuleElement('S', (0,), (2,)), MCFGRuleElement('NP', (0,)), MCFGRuleElement('VP', (2,)))
    test_object_from_string = MCFGRule.from_string('S(u, v) -> NP(u) VP(v)')
    epsilon_object = MCFGRule.from_string('N(human)')

    def test_object_creation(self):
        assert isinstance(self.test_object, MCFGRule)

    def test_to_tuple(self):
        assert self.test_object.to_tuple() == (self.test_object.left_side, self.test_object.right_side)

    def test_is_epsilon(self):
        assert self.test_object.is_epsilon is False
        assert self.epsilon_object.is_epsilon is True

    def test_left_side(self):
        assert self.test_object.left_side == MCFGRuleElement('S', (0,), (2,))

    def test_right_side(self):
        assert self.test_object.right_side == (MCFGRuleElement('NP', (0,)), MCFGRuleElement('VP', (2,)))

    def test_from_string(self):
        assert self.test_object_from_string == MCFGRule(MCFGRuleElement('S', (0,), (1,)), MCFGRuleElement('NP', (0,)), MCFGRuleElement('VP', (1,)))

    def test_unique_variable(self):
        assert self.test_object.unique_variables == {'S', 'NP', 'VP'}

    def test_string_yield(self):
        assert self.epsilon_object.string_yield() == 'N'

    def test_instantiate_left_side(self):
        rule = MCFGRule.from_string('S(w1u, x1v) -> NP(w1, x1) VP(u, v)')

        assert rule.instantiate_left_side(
            MCFGRuleElementInstance("NP", (1, 2), (5, 7)),
            MCFGRuleElementInstance("VP", (2, 4), (7, 8))
        ) == MCFGRuleElementInstance('S', (1,4,), (5, 8,))
