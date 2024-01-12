from ParsingTree.parsingtreerow import ParsingTreeRow


class OutputTree:
    def __init__(self, grammar):
        self.root = None
        self.grammar = grammar
        self.currentIndex = 1
        self.indexInInput = 1
        self.maxLevel = 0
        self.treeList = []

    def get_root(self):
        return self.root

    def generate_tree_from_sequence(self, input_sequence):
        production_index = input_sequence[0]
        production_string = self.grammar.get_ordered_productions()[production_index]

        self.root = ParsingTreeRow(production_string[0])
        self.root.set_index(0)
        self.root.set_level(0)

        self.root.set_left_child(self.build_recursive(1, self.root, production_string[1], input_sequence))
        return self.root

    def build_recursive(self, level, parent, current_content, input_sequence):
        if not current_content or self.indexInInput >= len(input_sequence) + 1:
            return None

        current_symbol = current_content[0]

        if current_symbol in self.grammar.get_terminals():
            node = ParsingTreeRow(current_symbol)
            node.set_index(self.currentIndex)
            self.currentIndex += 1
            node.set_level(level)
            node.set_parent(parent)

            new_list = current_content[1:]
            node.set_right_sibling(self.build_recursive(level, parent, new_list, input_sequence))
            return node

        elif current_symbol in self.grammar.get_non_terminals():
            production_index = input_sequence[self.indexInInput]
            production_string = self.grammar.get_ordered_productions()[production_index]

            node = ParsingTreeRow(current_symbol)
            node.set_index(self.currentIndex)
            node.set_level(level)
            node.set_parent(parent)

            new_level = level + 1
            if new_level > self.maxLevel:
                self.maxLevel = new_level

            self.currentIndex += 1
            self.indexInInput += 1

            node.set_left_child(self.build_recursive(new_level, node, production_string[1], input_sequence))
            new_list = current_content[1:]
            node.set_right_sibling(self.build_recursive(level, parent, new_list, input_sequence))
            return node
        else:
            print("ERROR")
            return None

    def print_tree(self, node, file_path):
        self.treeList = []
        self.create_list(node)

        with open(file_path, 'w') as f:
            for i in range(self.maxLevel + 1):
                for n in self.treeList:
                    if n.get_level() == i:
                        print(n)
                        f.write(str(n) + '\n')

    def write_to_file(self, file, line):
        with open(file, 'a') as f:
            f.write(line + '\n')

    def create_list(self, node):
        if node is None:
            return

        while node is not None:
            self.treeList.append(node)
            if node.get_left_child() is not None:
                self.create_list(node.get_left_child())

            node = node.get_right_sibling()
