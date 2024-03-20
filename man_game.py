import random 

f = open("voca.txt","r",encoding='UTF-8')
raw_data = f.read()
f.close()
print(raw_data.split("\n")[-1])
data_list = raw_data.split("\n")
data_list = data_list[:-1]
while True:
    r_index = random.randrange(0,len(data_list))
    word = data_list[r_index].replace(u"\xa0", u"").split(" ")[1]
    if len(word) <=6 : break

word = word.upper()
word_show = "_"*len(word)
print(word_show)
try_num = 0
ok_list = []
no_list = []

while True :
    ans = input().upper()
    print(ans)
    result = word.find(ans)
    print(result)
    
    if result == -1 :
        print("오답")
        try_num += 1 
        no_list.append(ans)
    else :
        print("정답")
        ok_list.append(ans)
        
        for i in range(len(word)):
            if word[i] == ans:
                word_show = word_show[:i] + ans + word_show[i+1:]
            print(word_show)
    if try_num == 7 : break 
    if word_show.find("_") == -1: break
print(word)
