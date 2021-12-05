import database as db

def check_usr_ans(message, test, score):
    user_ans = []
    right_ans = []  # массив правильных значений
    file = open(test, encoding="utf-8")
    for i in file.readlines()[::-1]:
        user_ans.append("".join(message.data.split("pl_")))
        row = i.split(";")
        right_answer = row[-1].split()[-1]  # переменная для добавки правильного ответа
        right_ans.append(right_answer)  # добавление верного значения
    file.close()
    for i in user_ans:
        if i in right_ans:
            score += 10
