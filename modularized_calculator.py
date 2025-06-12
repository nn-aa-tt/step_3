#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_multiply(line,index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1


def read_division(line,index):
    token = {'type': 'DIVISION'}
    return token, index + 1


def read_opening_parentheses(line,index):
    token = {'type': 'OPENING'}
    return token, index + 1


def read_closing_parentheses(line,index):
    token = {'type': 'CLOSING'}
    return token, index + 1


def read_abs(line, index):
    token = {'type': 'ABS'}
    return token, index + 3


def read_int(line, index):
    token = {'type': 'INT'}
    return token, index + 3


def read_round(line, index):
    token = {'type': 'ROUND'}
    return token, index + 5


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_division(line, index)
        elif line[index] == '(':
            (token, index) = read_opening_parentheses(line,index) 
        elif line[index] == ')':
            (token, index) = read_closing_parentheses(line,index) 
        elif line[index] == 'a' and line[index + 1] == 'b' and line[index + 2] == 's':
            (token, index) = read_abs(line,index)   
        elif line[index] == 'i' and line[index + 1] == 'n' and line[index + 2] == 't':
            (token, index) = read_int(line,index)  
        elif line[index] == 'r' and line[index + 1] == 'o' and line[index + 2] == 'u' and line[index + 3] == 'n' and line[index + 4] == 'd':
            (token, index) = read_round(line,index)  
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens



def evaluate_parentheses(tokens): #かっこに対応する
    new_tokens = [tokens[0]] #予め一つ目の要素（＋）を入れておく
    parentheses = [] #開きかっこのindexを記録する
    index = 1 
    opening_index = 0 #計算始めのindex
    closing_index = 0 #計算終わりのindex
    while index < len(tokens):
        if tokens[index]['type'] == 'OPENING':
            parentheses.append(index)
        elif tokens[index]['type'] == 'CLOSING':
            opening_index = parentheses.pop() + 1 #閉じかっこが現れたらoarenthesesから一つ要素を消し、opening_indexとして取得
            if len(parentheses) == 0: #要素数が０の時tokensの中で最も外側のかっこがとじている
                closing_index = index 
                res = {'type': 'NUMBER', 'number': evaluate(tokens[opening_index: closing_index])} #かっこの中を計算
                new_tokens.append(res)
        elif len(parentheses) == 0: #かっこの外側の場合
            new_tokens.append(tokens[index])
        index += 1

    return new_tokens


def evaluate_abs(tokens):
    index = 0
    new_tokens = []
    while index < len(tokens):
        res = 0
        if tokens[index]['type'] == 'ABS':
            if tokens[index + 1]['number'] < 0:
                res = tokens[index + 1]['number'] * -1
            else:
                res = tokens[index + 1]['number']
            new_tokens.append({'type': 'NUMBER', 'number': res})
            index += 2
        else:
            new_tokens.append(tokens[index])
            index += 1
    return new_tokens


def evaluate_int(tokens):
    index = 0
    new_tokens = []
    while index < len(tokens):
        if tokens[index]['type'] == 'INT':
            i = 0
            if tokens[index + 1]['number'] >= 0:
                while tokens[index + 1]['number'] - 1 >= i:
                    i += 1
            else:
                while tokens[index + 1]['number'] + 1 <= i:
                    i -= 1
            new_tokens.append({'type': 'NUMBER', 'number': i})
            index += 2
        else:
            new_tokens.append(tokens[index])
            index += 1
    return new_tokens

            
def evaluate_round(tokens): 
    index = 0
    new_tokens = []
    while index < len(tokens):
        if tokens[index]['type'] == 'ROUND':
            i = 0
            if tokens[index + 1]['number'] >= 0:
                while tokens[index + 1]['number'] >= i + 0.5:
                    i += 1
            else:
                while tokens[index + 1]['number'] <= i - 0.5:
                    i -= 1
            new_tokens.append({'type': 'NUMBER', 'number': i})
            index += 2
        else:
            new_tokens.append(tokens[index])
            index += 1
    return new_tokens


def evaluate_multiply_and_division(tokens):  #掛け算と割り算をする
    new_tokens = [tokens[0]] #新しいtokensを作る
    index = 1
    res = tokens[1] 
    if len(tokens) <= 2: #要素数が２以下の時そのまま返す
        return tokens
    while index < len(tokens) - 2:
        if tokens[index]['type'] == 'NUMBER': 
            if tokens[index + 1]['type'] == 'MULTIPLY':   #次の要素を見る
                res['number'] *= tokens[index + 2]['number'] #２つ先の要素と計算する
            elif tokens[index + 1]['type'] == 'DIVISION':
                res['number'] /= tokens[index + 2]['number']
            else:
                new_tokens.append(res) #現在のresを追加
                new_tokens.append(tokens[index + 1]) #+か-を追加
                res = tokens[index + 2] #resを2つ先の要素に更新
            index += 2
        if index == len(tokens) - 1:
            new_tokens.append(res)  #残り１つになったらresを追加
    return new_tokens


def evaluate_plus_and_minus(tokens):
    index = 1
    answer = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

    
def evaluate(tokens):
    if tokens[0]['type'] != 'MINUS':
        tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    tokens = evaluate_parentheses(tokens)
    tokens = evaluate_abs(tokens)
    tokens = evaluate_int(tokens)
    tokens = evaluate_round(tokens)
    tokens = evaluate_multiply_and_division(tokens)
    answer = evaluate_plus_and_minus(tokens)
    return answer

def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0*2.0+3/3")
    test("3*3*3")
    test("2*3-8")
    test("(3+2.1)*(3/(4-4.5))")
    test("(3.0+0*(2-1))/5")
    test("abs(-4)+abs(5+2*3)")
    test("int(1.5)+int(3.0)")
    test("-3+round(-1.5)+round(1.49)+round(0)")
    print("==== Test finished! ====\n")
run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
