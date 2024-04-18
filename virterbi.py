import numpy as np
import json
import sys
sensitivity=100 #可调参数
# 读取JSON文件
def read_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data
json_group_data={}
json_single_data={}
# 指定JSON文件名
json_group_file = './2_word.txt'
json_single_file='./1_word.txt'



def viterbi(pinyin):
    possibility=[]
    chinese=[]
    for i in pinyin:
        length=len(json_single_data[i][0])
        possibility.append(np.zeros(length))#第几个字对应的不同中文不同概率
        chinese.append(json_single_data[i][0])#中文索引
    score={}
    #初始化possibility
    step_way=[]
    start=[]
    dic={}
    try:
        for i in range(0,len(json_single_data[pinyin[0]][0])):
            start.append(-np.log(json_single_data[pinyin[0]][1][i]/json_single_data[pinyin[0]][2]))
            dic[json_single_data[pinyin[0]][0][i]]=json_single_data[pinyin[0]][0][i]
        
        possibility[0]=start
        step_way.append(dic)
    except:
        return;
    #last_word=[]
    end_word=[]
    tag=1
    for i in range(0,len(pinyin)-1):#逐个遍历
        path={}
        tag+=1
        for j in range(0,len(chinese[i+1])):
            mini=99999
            flag=0
            for k in range(0,len(chinese[i])):
                chinese_pair=chinese[i][k]+' '+chinese[i+1][j]
                pinyin_pair=pinyin[i]+' '+pinyin[i+1]
                
                try:
                    
                    com=-np.log(json_group_data[chinese_pair]/json_single_data[pinyin[i]][1][k])
                    score[chinese_pair]=com
                    if score[chinese_pair]+possibility[i][k]<mini:
                        mini=score[chinese_pair]+possibility[i][k]
                        min_word=chinese[i][k]
                        flag=k
                except:#如果在训练集中找不到
                    if sensitivity+possibility[i][k]<mini:
                        mini=sensitivity+possibility[i][k]
                        min_word=chinese[i][k]
                        flag=k
            possibility[i+1][j]=mini
            #step_way[i][chinese[i][flag]]+
            path[chinese[i+1][j]]=step_way[i][chinese[i][flag]]+min_word   
            if i==len(pinyin)-2:
                end_word.append(chinese[i+1][j])
                
        step_way.append(path)  
    min_index=np.argmin(possibility[-1])
    string=step_way[tag-1][chinese[tag-1][min_index]]
    ans=string[1:]+end_word[min_index]
    #print(ans)
    
    with open("../data/output.txt", "a") as file:
        file.write(ans + "\n")
sentence=[]
def read_and_process_txt(file_path):
    
    with open(file_path, 'r') as file:
        while True:
            line = file.readline()
            sentence.append(line.split())
            if not line:  
                break
     
'''      
    while True:
        try:
            line = input()
            if not line:
                break
            sentence.append(line.split())
            
        except EOFError:
            break
     '''
'''
    input_lines = sys.stdin.read().splitlines()
    sentence = [line.strip().replace(' ', '-') for line in input_lines]
'''
def ac(source):
    dicti = {}
    sum=0
    for key, value in source.items():
        lst = []
        counters = []
        for wd, cnt in zip(value["words"], value["counts"]):
            lst.append(wd)
            counters.append(cnt)
            sum+=cnt
        dicti[key]=[lst,counters,sum]
    return dicti

def acc(source):
    dicti = {}
    for key, value in source.items():
        for wd, cnt in zip(value["words"], value["counts"]):
            dicti[wd]=cnt
    return dicti

#main
# 读取JSON文件
json_group_data_o = read_json_file(json_group_file)
json_single_data_o=read_json_file(json_single_file)
json_single_data=ac(json_single_data_o)
json_group_data=acc(json_group_data_o)
file_path = "../data/std_input.txt" 
read_and_process_txt(file_path)
for i in sentence:
    viterbi(i)
