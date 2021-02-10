import re


class MathExpression():

    def __init__(self):
        # store integer values.
        self.digit_values = []
        # store operators values.
        self.ops_values = []

    @staticmethod
    def operation_order(op):
        """
        with this function we know what operation comes first. ^ then * and / then + and -
        :param op:
        :return:
        """
        if op == '+' or op == '-':
            return 1
        if op == '*' or op == '/':
            return 2
        if op == '^':
            return 3
        return 0

    @staticmethod
    def find_needed_operation(a, b, op):
        """
        given an operation, perform the needed action
        :param a:
        :param b:
        :param op:
        :return:
        """
        operations = {
            '+': a + b,
            '-': a - b,
            '*': a * b,
            '/': a // b,
            '^': a ** b
        }
        return operations.get(op)

    @staticmethod
    def get_power(p):
        """
        given a value for power, return the expresion of power that need to be in the equation.

        :param p:
        :return:
        """
        if p == 0:
            return ''
        elif p == 1:
            return '*x'
        else:
            return f'*x^{p}'

    def helper_calc_expression(self):
        """
        taks 2 numbers from self.digit_values, and an action from self.ops_values, and calculate the expression
        :return:
        """
        val2 = self.digit_values.pop()
        val1 = self.digit_values.pop()
        op = self.ops_values.pop()
        self.digit_values.append(self.find_needed_operation(val1, val2, op))

    def evaluate_expression(self, expresion):
        """
        given a string expression, evaluate the result. at this point the string contains only numbers and chars:
        +-*^()/. currently not supported sin and cos.
        the function run on the expresion, and check each char. if its a digit add it to list of digits. if its (
        add it to list of operation. if it operation (+-*/) -check the operation list. if the current operation is equal
        or smaller then the last operation we saw (that in the operation list)- calculate the last operation with the
        number we have, and then insert the new operation to the operation list.
        example: 2*3+5-4. for *: the first operation, we check and see the list is empty so we just add it to the
        operation list. when we get to +, we check and see that * comes before +. so we calculate 2*3=6, and now we have
        [+], [6,5]. when we come to - (which is like +), we calculate 6+5=11. and now we have [11,4],[-] which gives us
        7.

        :param expresion:
        :return:
        """
        # if expression empty
        if not expresion:
            return ''

        i = 0
        while i < len(expresion):

            # char is opening brace
            if expresion[i] == '(':
                self.ops_values.append(expresion[i])

            # char is closing brace, solve entire brace.
            elif expresion[i] == ')':
                while len(self.ops_values) != 0 and self.ops_values[-1] != '(':
                    self.helper_calc_expression()

                # pop opening brace.
                self.ops_values.pop()

            # char is a number
            elif expresion[i].isdigit():
                temp_val = 0
                # can be many digits
                while i < len(expresion) and expresion[i].isdigit():
                    temp_val = (temp_val * 10) + int(expresion[i])
                    i += 1

                self.digit_values.append(temp_val)
                # correct the offset (we get extra index in the while loop).
                i -= 1

            # char is an operator
            else:

                # check if top of ops_values has same or greater to current op apply operator on top of 'ops'.
                while (len(self.ops_values) != 0 and len(self.digit_values) >= 2 and self.operation_order(
                        self.ops_values[-1]) >= self.operation_order(expresion[i])):
                    self.helper_calc_expression()

                # add current operation to ops_values
                self.ops_values.append(expresion[i])

            i += 1

        # parsed all expression, apply remaining operation to remaining values.
        while len(self.ops_values) != 0:
            self.helper_calc_expression()

        # last value of digit_values contains result
        result = self.digit_values[-1]

        # empty list - maybe in the future we wants it to run always
        self.ops_values = []
        self.digit_values = []

        return result

    def polinom_derivation(self, expression):
        terms = expression.split('+')
        terms_map = []
        for term in terms:
            if 'x^' in term:
                coeff = int(term[:term.find('*x^')])
                power = int(term[term.find('x^') + 2:])
            elif 'x' in term:
                coeff = int(term[:term.find('*x')])
                power = 1
            else:
                coeff = int(term)
                power = 0
            terms_map.append((coeff, power))
        der_map = [(p * c, p - 1) for c, p in terms_map if p >= 1]  # if p=0 it is constant and not relevant
        str_terms = [(self.str_coeff(c, p) + self.get_power(p)) for c, p in der_map]
        der = '+'.join(str_terms)
        return der

    def str_coeff(self, c, p):
        if c == 1 and p == 0:
            return '1'
        return '' if c == 1 else str(c)

    def calc_der_sin_cos(self,sin_and_cos_list):
        new_sin_and_cos_der = []
        for exp in sin_and_cos_list:
            exp = exp[1:]
            if 'sin' in exp:
                inner_exp = exp[exp.find('sin*')+4:].replace('(','').replace(')','')
                temp = self.calculate_derivation(inner_exp)
                new_sin_and_cos_der.append(f"{exp.replace('sin','cos')}*{temp}")

            if 'cos' in exp:
                inner_exp = exp[exp.find('cos*')+4:].replace('(','').replace(')','')
                temp = self.calculate_derivation(inner_exp)
                new_sin_and_cos_der.append(f"{exp.replace('cos','sin')}*{temp}")
        return new_sin_and_cos_der

    def calculate_derivation(self, expression):
        all_terms = []
        in_parenthesis_regex = re.compile(r'\((.*?)\)')
        parenthesis_regex = re.compile(r'\d+\*\([^()]*\)\^\d')  # parenthesis expressions
        all_parenthesis = parenthesis_regex.findall(expression)
        not_pe = expression
        for t in all_parenthesis:  # take all terms that are not in  parenthesis
            not_pe = not_pe.replace(t, '')

        if not_pe:  # case of just parenthesis
            not_pe = not_pe[:-1] if not_pe[-1] in ['+', '-', '*', '/'] else not_pe
            if 'sin' in not_pe or 'cos' in not_pe:
                sin_and_cos_list = self.handle_sin_and_cos(not_pe)
                for temp_sin_cos in sin_and_cos_list:
                    not_pe = not_pe.replace(temp_sin_cos,'')
                sin_and_cos_list = self.calc_der_sin_cos(sin_and_cos_list)
                all_terms.extend(sin_and_cos_list)

            all_terms.append(self.polinom_derivation(not_pe))

        # for each parenthesis, calculate inner derivation. not support inner ()
        for t in all_parenthesis:
            t1 = in_parenthesis_regex.findall(t)[0]
            coeff = t.split('*(')[0]
            power = int(t.split(')^')[1])
            poli_derv = self.polinom_derivation(t1)
            if power == 1:
                deriv = f"{coeff}*{power}*({poli_derv})"
            else:
                deriv = f"{coeff}*{power}*{poli_derv}*({t1})^{int(power) - 1}"

            all_terms.append(deriv)
        return '+'.join(all_terms)

    def handle_sin_and_cos(self, expression):
        """
        if we have sin/cos in the expresion - we handel them seperaitly from the total expresion
        :param expression:
        :return:
        """
        sin_and_cos_expressions = []
        if 'sin' in expression or 'cos' in expression:
            sin_regex = re.compile(r'\+*-*\^*/*\d*sin\*\(*\d*\**\d*\)*x*\)*')
            cos_regex = re.compile(r'\+*-*\^*/*\d*cos\*\(*\d*\**\d*\)*x*\)*')
            all_sin = sin_regex.findall(expression)
            all_cos = cos_regex.findall(expression)
            sin_and_cos_expressions = all_sin + all_cos
        return sin_and_cos_expressions

    def evaluate_sin_and_cos(self, sin_and_cos_expressions):
        """
        for each sin/cos we have - calculate the expresion in there parenthesis
        :param sin_and_cos_expressions:
        :return:
        """
        in_parenthesis_regex = re.compile(r'\((.*?)\)')
        sin_cos_regex = re.compile(r'\d*sin|cos')
        new_sin_and_cons = []
        for epx in sin_and_cos_expressions:
            new_epx = in_parenthesis_regex.findall(epx)[0]
            starter = sin_cos_regex.findall(epx)[0]
            new_eval = self.evaluate_expression(new_epx)
            new_sin_and_cons.append(f"+{starter}{new_eval}")
        return new_sin_and_cons


def calculate_options(option, expression, x_val=None):
    """
    given the option we got from the user, perform the wanted action.

    :param option:
    :param expression:
    :return:
    """
    math_expresion = MathExpression()
    expression = expression.replace(' ', '').replace('x', '*x').replace('(', '*(').replace('(*', '(1*').replace('(+',
                                                                                                                '(1+').replace(
        '(-', '(1-').replace('(/', '(1/')

    if option == '1':
        original_expression = expression
        if x_val is None:
            x_val = input("please insert x value: ")
        expression = expression.replace('x', x_val)

        # if we have sin and cos in data - handle them separately
        sin_and_cos_expressions = math_expresion.handle_sin_and_cos(expression)
        for sin_cos in sin_and_cos_expressions:
            expression = expression.replace(sin_cos, '')

        evaluation = math_expresion.evaluate_expression(expression)
        sin_and_cos_expressions = math_expresion.evaluate_sin_and_cos(sin_and_cos_expressions)
        print(sin_and_cos_expressions)
        if sin_and_cos_expressions:
            evaluation = f"{evaluation}{''.join(sin_and_cos_expressions)}"
        print(f"The evaluation for expression: {original_expression} is: {evaluation}")
        return evaluation

    if option == '2':
        print(expression)
        derivation = math_expresion.calculate_derivation(expression)
        print(derivation)
        return derivation

    if option == '3':
        print(expression)
        derivation = math_expresion.calculate_derivation(expression)
        print(derivation)
        new_expression = derivation.replace('x', x_val)
        print("new expression is: ", new_expression)
        evaluation = math_expresion.evaluate_expression(new_expression)
        print(f"The evaluation for expression: {new_expression} is: {evaluation}")
        return evaluation


def main():
    # assumption -> before x always comes with number. even if 1
    # assumption -> before ( always comes with number, even if 1(
    # assumption -> before ) always comes with ^number, even if )^1

    expression = input("hello please insert expression: ")
    option = input("""do you want to:
    1. evaluate the expression
    2. calculate expression derivation
    3. calculate expression derivation and evaluate derivation\n""")
    calculate_options(option, expression)


if __name__ == "__main__":
    # main()

    # tests
    math_exp = MathExpression()
    #print(calculate_options('1', '1x+1sin(3x)+2cos(2x)', '2'))
    assert calculate_options('1', '1x+1sin(3x)+2cos(2x)', '2') == '2+1sin6+cos4'
    assert calculate_options('1','2x+5-4','3') == 7
    assert calculate_options('1','2x^2+5x-4','2') == 14
    assert calculate_options('1', '2x^2+5x-4(x^2)','2') == 2
    assert math_exp.evaluate_expression('2*3+5-4') == 7
    assert math_exp.evaluate_expression('1*5^2+2*5+1') ==36
    assert math_exp.evaluate_expression('2*1^3+1*(3*1+5)^2') == 66
    assert math_exp.evaluate_expression('2') == 2
    assert math_exp.evaluate_expression('') == ''
    assert math_exp.evaluate_expression('2*3^5+9*3+12+2*(2*3*4)^2') == 1677
    assert math_exp.evaluate_expression('3*4*(2+4)^2') == 432
    assert math_exp.evaluate_expression('9/3*(2+4)^2') == 108

    assert calculate_options('2', '2x^2+5x-4(x^2)^2+2+3x^2+2(2x+1)^2','2') == '4*x+5+6*x+4*2*2*x*(1*x^2)^1+2*2*2*(2*x+1)^1'
    assert calculate_options('2', '2(2x+1)^2','2') == '2*2*2*(2*x+1)^1'
    assert calculate_options('3', '2(2x+1)^2','2') == 40
