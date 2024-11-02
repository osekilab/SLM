import json
from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *

class AgreementGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="morphology",
                         linguistics="irregular_forms",
                         uid="overregularized_past_verbs_aochildes",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=False)
        self.all_trans_en_verbs = get_all("irr_verb", "1", all_transitive_verbs)     # 他動詞
        self.all_intrans_en_verbs = get_all("irr_verb", "1", all_intransitive_verbs) # 自動詞
        self.all_cds_nouns = get_all("is_in_cds", "1", all_nouns)
        with open('verb2type.json') as f:
            self.verb2type = json.load(f)
            

    def sample(self):
        # John ate    the pie
        # N1   V_past     N2
        # John eated  the pie
        # N1   V_over      N2

        x = random.random()
        if x < 1 / 2:
            V_base = choice(self.all_trans_en_verbs)
            N2 = N_to_DP_mutate(choice(get_matches_of(V_base, "arg_2", self.all_cds_nouns)))
        else:
            V_base = choice(self.all_intrans_en_verbs)
            N2 = " "

        Verbs = get_all("root", V_base["root"])
        V_past = get_all("past", "1", Verbs)
        V_bare = get_all("bare", "1", Verbs)
        V_past_ed = get_all("past_ed", "1", Verbs)
        V_base_ed = get_all("base_ed", "1", Verbs)
        N1 = N_to_DP_mutate(choice(get_matches_of(V_base, "arg_1", self.all_cds_nouns)))

        data = {
            "sentence_good": "%s %s %s." % (N1[0], V_past[0][0], N2[0]),
            "sentence_base-ed": "%s %s %s." % (N1[0], V_base_ed[0][0], N2[0]),
            "sentence_past-ed": "%s %s %s." % (N1[0], V_past_ed[0][0], N2[0]),
            "sentence_copy": "%s %s %s." % (N1[0], V_bare[0][0], N2[0]),
            "one_prefix_prefix": "%s" % (N1[0]),
            "one_prefix_word_good": V_past[0][0],
            "one_prefix_word_base-ed": V_base_ed[0][0],
            "one_prefix_word_past-ed": V_past_ed[0][0],
            "one_prefix_word_copy": V_bare[0][0],
            "verb_type": self.verb2type[V_bare[0][0]],
        }
        return data, data["sentence_good"]

generator = AgreementGenerator()
generator.generate_paradigm(rel_output_path="outputs/%s.jsonl" % generator.uid)
