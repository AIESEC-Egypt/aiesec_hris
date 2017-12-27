def compare_lists(qs1=None, qs2=None, field=None, first_list_is_dict=False):
    """
    Compare unordered equivelence of `qs1` and `qs2`

    :field: field to compare over

    Author: Nader Alexan
    """
    # make copy to avoid chagining original list
    for queryset_item in qs2:
        found = False
        for item in qs1:
            if first_list_is_dict:
                val = item.get(field)
            else:
                val = getattr(item, field)
            if val == getattr(queryset_item, field):
                found = item
                break
        if not found:
            return False
    return len(qs1) == len(qs2)


def compare_object(json_obj, obj):
    """
    Compare the equality of key, value pairs
    of a json(dictionary) object `json_obj`
    with the field of a python object `obj`
    Author: Nader Alexan
    """
    for key in json_obj.keys():
        if getattr(obj, key) != json_obj.get(key):
            return False
    return True
