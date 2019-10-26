from typing import List, Set


# FuzzySearch was created so that we could quickly scan for any notices of
# "probation revoked", including any typos and ignoring casing.
class FuzzySearch:
    @staticmethod
    def search(text: str, search_terms: List[str]) -> bool:
        lower_case_text = text.lower()
        lower_case_search_terms = [term.lower() for term in search_terms]
        for term in lower_case_search_terms:
            fuzzed_terms = FuzzySearch.__edits(term)
            for fuzzed_term in fuzzed_terms:
                if fuzzed_term in lower_case_text:
                    return True
        return False

    # Adapted from http://norvig.com/spell-correct.html
    @staticmethod
    def __edits(word) -> Set[str]:
        "All edits that are one edit away from `word`."
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)
