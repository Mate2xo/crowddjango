class Null:
    """Does nothing and is Falsy"""

    def __init__(self, *_, **__): pass
    def __call__(self, *_, **__): return None
    def __repr__(self): return ""
    def __nonzero__(self): return 0

    def __eq__(self, object) -> bool:
        return True if object is None else False

    def __getattr__(self, _): return None
    def __setattr__(self, _, __): return None
    def __delattr__(self, _): return None
