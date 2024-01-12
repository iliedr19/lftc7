import re
from Scanner.symboltable import SymbolTable
from Scanner.programinternalform import ProgramInternalForm
from Utils.pair import Pair


class MyScanner:
    def __init__(self, file_path):
        self.operators = ["+", "-", "*", "/", "%", "<=", ">=", "==", "!=", "<", ">", "="]
        self.separators = ["{", "}", "(", ")", "[", "]", ":", ";", " ", ",", "\t", "\n", "'", "\""]
        self.reserved_words = ["spatiu", "linie_noua", "citeste", "scrie", "daca", "altfel", "pentru", "cat_timp",
                               "returneaza", "start", "finish", "tab", "int", "string", "char", "array"]
        self.file_path = file_path
        self.symbol_table = SymbolTable(100)
        self.pif = ProgramInternalForm()

    def read_file(self):
        try:
            with open(self.file_path, 'r') as file:
                content = file.read().replace('\t', '')
            return content
        except FileNotFoundError as e:
            print(e)
            return None

    def create_list_of_program_elems(self):
        content = self.read_file()
        if content is None:
            return None

        # Split content into words
        words = re.findall(r'[a-zA-Z_]\w*|[+\-*/%=<>!]=?|[-+]?\d+|\S', content)

        # Escape metacharacters in separators
        separators_string = ''.join(re.escape(sep) for sep in self.separators)

        # Tokenize words
        tokens = []
        for word in words:
            subtokens = re.split(f'({separators_string})', word)
            tokens.extend(self.tokenize(subtokens))

        for t in tokens:
            print(t)
        return tokens

    def tokenize(self, tokens_to_be):
        resulted_tokens = []
        is_string_constant = False
        is_char_constant = False
        created_string = ''
        number_line = 1
        number_column = 1

        for t in tokens_to_be:
            if t == "\"":
                if is_string_constant:
                    created_string += t
                    resulted_tokens.append(Pair(created_string, Pair(number_line, number_column)))
                    created_string = ''
                else:
                    created_string += t
                is_string_constant = not is_string_constant

            elif t == "'":
                if is_char_constant:
                    created_string += t
                    resulted_tokens.append(Pair(created_string, Pair(number_line, number_column)))
                    created_string = ''
                else:
                    created_string += t
                is_char_constant = not is_char_constant

            elif t == "\n":
                number_line += 1
                number_column = 1

            else:
                if is_string_constant:
                    created_string += t
                elif is_char_constant:
                    created_string += t
                elif t != " ":
                    resulted_tokens.append(Pair(t, Pair(number_line, number_column)))
                    number_column += 1

        return resulted_tokens

    def scan(self):
        tokens = self.create_list_of_program_elems()
        if tokens is None:
            return

        lexical_error_exists = False

        for t in tokens:
            token = t.get_first()
            if token in self.reserved_words:
                self.pif.add(Pair(token, Pair(-1, -1)), 2)
            elif token in self.operators:
                self.pif.add(Pair(token, Pair(-1, -1)), 3)
            elif token in self.separators:
                self.pif.add(Pair(token, Pair(-1, -1)), 4)
            elif re.match(r'^0|[1-9][0-9]*|[a-zA-Z]|\'[1-9]\'|\'[a-zA-Z]\'|\"[0-9]*[a-zA-Z ]*\"$', token):
                self.symbol_table.add(token)
                self.pif.add(Pair(token, self.symbol_table.find_position_of_term(token)), 0)
            elif re.match(r'^([a-zA-Z]|_)[a-zA-Z_0-9]*$', token):
                self.symbol_table.add(token)
                self.pif.add(Pair(token, self.symbol_table.find_position_of_term(token)), 1)
            else:
                pair_line_column = t.get_second()
                print(f"Error at line: {pair_line_column.get_first()} and column: {pair_line_column.get_second()}, invalid token: {t.get_first()}")
                lexical_error_exists = True

        if not lexical_error_exists:
            print("Program is lexically correct!")

    def get_pif(self):
        return self.pif

    def get_symbol_table(self):
        return self.symbol_table