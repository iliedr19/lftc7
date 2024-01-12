class ParsingTable:
    def __init__(self):
        self.entries = []

    def __str__(self):
        result = "Parsing Table: \n"
        for entry in self.entries:
            result += str(entry) + "\n"
        return result
