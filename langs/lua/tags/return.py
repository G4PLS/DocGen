from DocMatcher.docTag import ParameterDocTag

class ReturnDocTag(ParameterDocTag):
    NAME: str = "return"
    SPLIT: int = 1

    def __init__(self, file_path: str, line_number: int, data: str):
        self.type: str
        self.value: str
        self.description: str

        super().__init__(file_path, line_number, data)

    def parse_data(self, data: str):
        parts = self.split_data(data)
        
        # type is always first
        self.type = parts[0]

        if len(parts) == 1:
            self.value = ""
            self.description = ""
            return

        rest = parts[1].strip()

        # If value starts with { or [, capture until matching }
        if rest.startswith("{"):
            depth = 0
            value_chars = []
            i = 0
            while i < len(rest):
                c = rest[i]
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                value_chars.append(c)
                i += 1
                if depth == 0:
                    break
            self.value = "".join(value_chars).strip()
            self.description = rest[i:].strip()
        else:
            # fallback: next word is value, rest is description
            value_parts = rest.split(maxsplit=1)
            self.value = value_parts[0]
            self.description = value_parts[1] if len(value_parts) > 1 else ""

    def json(self):
        return {
            "type": self.TYPE,
            "tag-type": self.NAME,
            "return-type": self.type,
            "return-value": self.value,
            "return-description": self.description
        }