from docgen.DocMatcher.docBlock import DocBlock
from ..tags.default import DefaultDocTag
from ..tags.desc import DescriptionDocTag
from ..tags.author import AuthorDocTag
from ..tags.realm import RealmDocTag
from ..tags.flags import FlagsDocTag

class ConVar(DocBlock):
    NAME = "convar"
    ALLOWED_TAGS = [DefaultDocTag, DescriptionDocTag, AuthorDocTag, RealmDocTag, FlagsDocTag]