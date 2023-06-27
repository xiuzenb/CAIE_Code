from src.AST.data import *

class Statements:
    def __init__(self):
        self.type = 'STATEMENTS'
        self.statements = []

    def add_statement(self, statement):
        self.statements.append(statement)

    def get_tree(self, level=0):
        result = ''
        for statement in self.statements:
            result += '\n' + statement.get_tree(level)
        return result

    def exe(self):
        result = []
        for statement in self.statements:
            try:
                result.append(statement.exe())
            except:
                print(self.get_tree())

        return result

class If:
    def __init__(self, condition, true_statement, false_statement=None):
        self.type = 'IF'
        self.condition = condition
        self.true_statement = true_statement
        self.false_statement = false_statement

    def get_tree(self, level=0):
        result = LEVEL_STR * level
        result += 'IF\n' + self.condition.get_tree(level+1)
        result += '\n' + self.true_statement.get_tree(level+1)
        result += ( 'ELSE\n' + self.false_statement.get_tree(level+1) ) if self.false_statement else ''

        return result

    def exe(self):
        if self.condition.exe()[0]:
            self.true_statement.exe()
        else:
            if self.false_statement:
                self.false_statement.exe()

class For:
    def __init__(self, id, left, right, body_statement, next_id):
        self.type = 'FOR'
        self.id = id
        self.left = left
        self.right = right
        self.body_statement = body_statement
        self.next_id = next_id

    def get_tree(self, level=0):
        result = LEVEL_STR * level
        result += 'FOR\n' + str(self.id)
        result += '\n' + self.left.get_tree(level+1) + '\n' + str(self.right.get_tree(level+1))
        result += 'NEXT\n' + str(self.next_id)

    def exe(self):
        left = self.left.exe()
        right = self.right.exe()
        if left[1] == 'INTEGER' and right[1] == 'INTEGER':
            for i in range(left[0], right[0]+1):
                # 给 index 赋值
                stack.new_variable(self.id, 'INTEGER')
                stack.set_variable(self.id, i, 'INTEGER')
                # 执行内部操作
                self.body_statement.exe()
                # 核对id是否相同
                if self.id == self.next_id:
                    continue
                else:
                    print(f'Expect `{self.id}` for next id, but found `{self.next_id}`')
                    break
        else:
            print(f'Expect `INTEGER` for index, but found `{left[1]}` and `{right[1]}`. ')

class Case:
    def __init__(self, id, cases):
        self.type = 'CASE'
        self.id = id
        self.cases = cases

    def get_tree(self, level=0):
        return LEVEL_STR * level + self.type + '\n' + str(self.id) + '\n' + self.cases.get_tree

    def exe(self):
        value = stack.get_variable(self.id)
        self.cases.exe(value)

class Cases:
    def __init__(self):
        self.type = 'CASES'
        self.cases = []
        self.otherwise = None

    def get_tree(self, level=0):
        result = LEVEL_STR * level + self.type
        for i in self.cases:
            result += '\n' + i.get_tree(level+1)
        return result

    def add_case(self, case):
        if case.is_otherwise:
            self.otherwise = case
        else:
            self.cases.append(case)

    def exe(self, value):
        for case in self.cases:
            if case.check(value):
                case.exe()
                break
        else:
            if self.otherwise:
                self.otherwise.exe()

class A_case:
    def __init__(self, condition, true_statement, is_otherwise=False):
        self.type = 'A_CASE'
        self.condition = condition
        self.true_statement = true_statement
        self.is_otherwise = is_otherwise

    def get_tree(self, level=0):
        return LEVEL_STR * level + self.type + '\n' + self.condition.get_tree(level+1) + '\n' + self.true_statement.get_tree(level+1)

    def check(self, value):
        if self.condition.type == 'RANGE':
            r = set(self.condition.exe())
        else:
            r = {self.condition.exe()}

        return value in r

    def exe(self):
        self.true_statement.exe()

class Range:
    def __init__(self, start, end):
        self.type = 'RANGE'
        self.start = start
        self.end = end

    def get_tree(self, level=0):
        return LEVEL_STR * level + self.type + '\n' + self.start.get_tree(level+1) + '\n' + self.end.get_tree(level+1)

    def exe(self):
        n1 = self.start.exe()
        n2 = self.end.exe()
        if n1[1] == 'INTEGER' and n2[1] == 'INTEGER':
            l = []
            for i in range(n1[0], n2[0]+1):
                l.append((i, 'INTEGER'))
            return l
        else:
            print(f'Expect `INTEGER` for a range argument, but found `{n1[1]}` and `{n2[1]}`')

class Repeat:
    def __init__(self, true_statement, condition):
        self.type = 'REPEAT'
        self.true_statement = true_statement
        self.condition = condition

    def get_tree(self, level=0):
        return LEVEL_STR * level + self.type + '\n' + self.true_statement.get_tree(level+1) + '\n' + self.condition.get_tree(level+1)

    def exe(self):
        while 1:
            self.true_statement.exe()
            if self.condition.exe()[0]:
                break
