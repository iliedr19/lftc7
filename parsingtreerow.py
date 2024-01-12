class ParsingTreeRow:
    def __init__(self, info):
        self.index = None
        self.info = info
        self.parent = None
        self.rightSibling = None
        self.leftChild = None
        self.level = None

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def get_info(self):
        return self.info

    def set_info(self, info):
        self.info = info

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_right_sibling(self):
        return self.rightSibling

    def set_right_sibling(self, right_sibling):
        self.rightSibling = right_sibling

    def get_left_child(self):
        return self.leftChild

    def set_left_child(self, left_child):
        self.leftChild = left_child

    def get_level(self):
        return self.level

    def set_level(self, level):
        self.level = level

    def __str__(self):
        result = "ParsingTree.ParsingTreeRow: "
        result += f"index = {self.index}, info = {self.info}, "
        result += f"leftChild = {self.leftChild.get_index() if self.leftChild else -1}, "
        result += f"rightChild = {self.rightSibling.get_index() if self.rightSibling else -1}, "
        result += f"parent = {self.parent.get_index() if self.parent else -1}, "
        result += f"level = {self.level}"
        return result
