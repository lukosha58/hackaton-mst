def check_usr_ans(message, test,score):
    user_ans = []
    right_ans = []
    file = open(test, encoding="utf-8")
    for i in file.readlines()[::-1]:
        user_ans.append("".join(message.data.split("pl_")))
        row = i.split(";")
        right_answer = row[-1].split()[-1]
        right_ans.append(right_answer)
    file.close()
    for i in user_ans:
        if i in right_ans:
            score += 10/len(right_ans)  # типа рейтинг
    print(score)