from collections import defaultdict

context = defaultdict(dict)


def context_for(pid):
    return context[pid]
