from src.docMatcher import ParameterDocTag

class ParamDocTag(ParameterDocTag):
    NAME: str = "param"
    SPLIT: int = 2

    def __init__(self, file_path: str, line_number: int, data: str):
        self.type: str
        self.variable_name: str
        self.description: str

        super().__init__(file_path, line_number, data)

    def parse_data(self, data: str):
        parts = self.split_data(data)

        self.type = parts[0]
        self.variable_name = parts[1]
        self.description = parts[2] if len(parts) > 2 else ""

    def json(self):
        return {
            "type": "PARAM",
            "tag-type": self.NAME,
            "variable-type": self.type,
            "variable-name": self.variable_name,
            "variable-description": self.description
        }