def scrub(obj, bad="type"):
    """
    Scrub the _type dict item recursively

    Credit through Athony Shaw: https://stackoverflow.com/a/20692955/7402337

    """
    if isinstance(obj, dict):
        for k in list(obj.keys()):
            if k == bad:
                del obj[k]
            else:
                scrub(obj[k], bad)
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            if obj[i] == bad:
                del obj[i]
            else:
                scrub(obj[i], bad)

    else:
        # neither a dict nor a list, do nothing
        pass
