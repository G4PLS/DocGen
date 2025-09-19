from docgen.DocMatcher.docTag import ParameterDocTag

class ParamDocTag(ParameterDocTag):
    NAME: str = "param"
    SPLIT: int = 2

    def __init__(self, file_path: str, data: str):
        self.type: str
        self.variable_name: str
        self.description: str

        super().__init__(file_path, data)

    def parse_data(self, data: str):
        super().parse_data(data)
        parts = self.split_data(data)

        self.type = parts[0]
        self.variable_name = parts[1]
        self.description = parts[2] if len(parts) > 2 else ""

    def json(self):
        data = super().json()

        data["variable-type"] = self.type
        data["variable-name"] = self.variable_name
        data["variable-description"] = self.description

        return data