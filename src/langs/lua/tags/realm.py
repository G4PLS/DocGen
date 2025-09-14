from src.docMatcher import StateDocTag

class RealmDocTag(StateDocTag):
    NAME: str = "realm"
    STATES: list[str] = ["server", "client", "shared"]