from collections import deque, defaultdict
from itertools import product
from typing import List
from src.mcfg_parser_aditya_dan.grammar import *
from src.mcfg_parser_aditya_dan.tree import *


class Parser:
    """
    Parse sentences using a MCFG.

    Parameters
    ----------
    rules : list of MCFGRule
        The rules in the MCFG.

    Attributes
    ----------
    rules : list of MCFGRule
        The rules in the MCFG.
    chart : set of MCFGRuleElementInstance
        The set of all instantiated rule elements.
    agenda : deque of MCFGRuleElementInstance
         Queue of elements not yet processed.
    grammar_by_rhs : dict
        Maps tuples of RHS variable names to lists of rules.
    """

    def __init__(self, rules: List[MCFGRule]):
        self.rules = rules
        self.chart = set()
        self.agenda = deque()
        self.grammar_by_rhs = defaultdict(list)

        for rule in rules:
            if not rule.is_epsilon:
                key = tuple(element.variable for element in rule.right_side)
                self.grammar_by_rhs[key].append(rule)

    def initialize_lexical_rules(self, sentence: List[str]):
        """Add all matching lexical rules to agenda

            Parameters
            ----------
            sentence : list of str
                The sentence being parsed.
        """

        for i, word in enumerate(sentence):
            for rule in self.rules:
                if rule.is_epsilon:
                    inst = MCFGRuleElementInstance(rule.left_side.variable, (i, i + 1))
                    self.agenda.append(inst)
                    self.chart.add(inst)

    def parse(self, sentence: List[str]) -> List[MCFGRuleElementInstance]:

        """Parses the sentence

            Parameters
            ----------
            sentence : list of str
                The sentence being parsed.
        """

        self.chart.clear()
        self.agenda.clear()
        self.initialize_lexical_rules(sentence)

        completed = []

        while self.agenda:
            item = self.agenda.popleft()

            # Consider all rules that may use this item
            for rule in self.rules:
                if rule.is_epsilon:
                    continue

                num_rhs = len(rule.right_side)

                # Collect combinations of chart entries
                candidates = [
                    entry for entry in self.chart
                    if entry.variable in [el.variable for el in rule.right_side]
                ]

                def try_expand(existing_entries, depth=0):
                    if depth == num_rhs:
                        try:
                            new_instance = rule.instantiate_left_side(*existing_entries)
                            if new_instance not in self.chart:
                                self.chart.add(new_instance)
                                self.agenda.append(new_instance)
                                if new_instance.variable == 'S' and new_instance.string_spans[0] == (0, len(sentence)):
                                    completed.append(new_instance)
                        except ValueError:
                            pass
                        return

                    for cand in candidates:
                        if cand.variable == rule.right_side[depth].variable:
                            try_expand(existing_entries + [cand], depth + 1)

                try_expand([])

        return completed

    def build_trees(self, node, forest):
        """
        Recursively constructs all parse-trees for a given instance node.

        Parameters
        ----------
        node : MCFGRuleElementInstance
            A chart entry instance to expand into Trees.
        forest : dict
            Mapping from MCFGRuleElementInstance to a list of tuples
        Returns
        -------
        List[Tree]
            All possible subtree roots under node.
        """

        if node not in forest or not forest[node]:
            return [Tree(node.variable, node.string_spans, [])]

        trees = []

        for rule, children in forest[node]:
            # Recursively build subtrees for each child
            child_trees_lists = [self.build_trees(child, forest) for child in children]
            # Combine all child tree alternatives
            for combo in product(*child_trees_lists):
                trees.append(Tree(node.variable, node.string_spans, list(combo)))
        return trees
