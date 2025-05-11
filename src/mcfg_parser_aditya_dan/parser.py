from collections import deque, defaultdict
from typing import List
from grammar import *


class Parser:
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
        """Add all matching lexical rules to agenda."""
        for i, word in enumerate(sentence):
            for rule in self.rules:
                if rule.is_epsilon:
                    inst = MCFGRuleElementInstance(rule.left_side.variable, (i, i + 1))
                    self.agenda.append(inst)
                    self.chart.add(inst)

    def parse(self, sentence: List[str]) -> List[MCFGRuleElementInstance]:
        self.chart.clear()
        self.agenda.clear()
        self.initialize_lexical_rules(sentence)

        completed = []

        while self.agenda:
            item = self.agenda.popleft()

            # Consider all rules that might use this item
            for rule in self.rules:
                if rule.is_epsilon:
                    continue

                num_rhs = len(rule.right_side)

                # Gather combinations of matching chart entries
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


rule_list = ['S(uv) -> NP(u) VP(v)',
             'S(uv) -> NPwh(u) VP(v)',
             'S(vuw) -> Aux(u) Swhmain(v, w)',
             'S(uwv) -> NPdisloc(u, v) VP(w)',
             'S(uwv) -> NPwhdisloc(u, v) VP(w)',
             'Sbar(uv) -> C(u) S(v)',
             'Sbarwh(v, uw) -> C(u) Swhemb(v, w)',
             'Sbarwh(u, v) -> NPwh(u) VP(v)',
             'Swhmain(v, uw) -> NP(u) VPwhmain(v, w)',
             'Swhmain(w, uxv) -> NPdisloc(u, v) VPwhmain(w, x)',
             'Swhemb(v, uw) -> NP(u) VPwhemb(v, w)',
             'Swhemb(w, uxv) -> NPdisloc(u, v) VPwhemb(w, x)',
             'Src(v, uw) -> NP(u) VPrc(v, w)',
             'Src(w, uxv) -> NPdisloc(u, v) VPrc(w, x)',
             'Src(u, v) -> N(u) VP(v)',
             'Swhrc(u, v) -> Nwh(u) VP(v)',
             'Swhrc(v, uw) -> NP(u) VPwhrc(v, w)',
             'Sbarwhrc(v, uw) -> C(u) Swhrc(v, w)',
             'VP(uv) -> Vpres(u) NP(v)',
             'VP(uv) -> Vpres(u) Sbar(v)',
             'VPwhmain(u, v) -> NPwh(u) Vroot(v)',
             'VPwhmain(u, wv) -> NPwhdisloc(u, v) Vroot(w)',
             'VPwhmain(v, uw) -> Vroot(u) Sbarwh(v, w)',
             'VPwhemb(u, v) -> NPwh(u) Vpres(v)',
             'VPwhemb(u, wv) -> NPwhdisloc(u, v) Vpres(w)',
             'VPwhemb(v, uw) -> Vpres(u) Sbarwh(v, w)',
             'VPrc(u, v) -> N(u) Vpres(v)',
             'VPrc(v, uw) -> Vpres(u) Nrc(v, w)',
             'VPwhrc(u, v) -> Nwh(u) Vpres(v)',
             'VPwhrc(v, uw) -> Vpres(u) Sbarwhrc(v, w)',
             'NP(uv) -> D(u) N(v)',
             'NP(uvw) -> D(u) Nrc(v, w)',
             'NPdisloc(uv, w) -> D(u) Nrc(v, w)',
             'NPwh(uv) -> Dwh(u) N(v)',
             'NPwh(uvw) -> Dwh(u) Nrc(v, w)',
             'NPwhdisloc(uv, w) -> Dwh(u) Nrc(v, w)',
             'Nrc(v, uw) -> C(u) Src(v, w)',
             'Nrc(u, vw) -> N(u) Swhrc(v, w)',
             'Nrc(u, vwx) -> Nrc(u, v) Swhrc(w, x)',
             'Dwh(which)',
             'Nwh(who)',
             'D(the)',
             'D(a)',
             'N(greyhound)',
             'N(human)',
             'Vpres(believes)',
             'Vroot(believe)',
             'Aux(does)',
             'C(that)']

MCFG_rules = []

for rule_string in rule_list:
    MCFG_rule = MCFGRule.from_string(rule_string)
    MCFG_rules.append(MCFG_rule)

parser = Parser(MCFG_rules)

print(parser.parse(['who', 'does', 'the', 'greyhound', 'believe']))
