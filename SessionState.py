class _SessionState:
    def __init__(self):
        self.__dict__ = {}

def _get_state():
    """Create a SessionState object if not already exists."""
    global _session_state
    if '_session_state' not in globals():
        _session_state = _SessionState()
    return _session_state
