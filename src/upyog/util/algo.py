def find_best_groups(items, wkey, threshold):
    n_items = len(items)
    groups  = []

    total   = 0

    if isinstance(wkey, str):
        key  = wkey
        wkey = lambda item: item[key]

    def _backtrack(start, group, weight, used):
        nonlocal groups, total

        if total > threshold:
            return
        
        if start == n_items:
            if group:
                sum_ = sum(wkey(item) for item in group)
                if sum_ > total:
                    groups = [group[:]]
                    total  = sum_
                elif sum_ == total:
                    groups.append(group[:])

            return

        if not used[start]:
            group.append(items[start])
            used[start] = True
            _backtrack(start + 1, group, weight + wkey(items[start]), used)
            used[start] = False
            group.pop()

        _backtrack(start + 1, group, weight, used)

    used   = [False] * n_items
    _backtrack(0, [], 0, used)
    return groups