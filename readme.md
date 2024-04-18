# 人工智能导论-拼音输入法作业
基于viterbi和二元词统计的全拼拼音输入法
### 关于命令行重定向
    需要将Viterbi.py中输入部分注释掉的代码取消注释，并注释或删除掉打开读取input文件的代码
    
    具体的：
    
```python
    input_lines = sys.stdin.read().splitlines()
    sentence = [line.strip().replace(' ', '-') for line in input_lines]
```
## 内容

* ### 训练代码部分
    *  single_word训练：统计单个字出现频率值，按照拼音分类存放
    *  group_words训练：统计二元词组出现频率，按照拼音分类存放
* ### Viterbi部分
    通过逐层迭代并记录父节点的方法得到栅栏图的最短路径，也就是概率最高的中文结果

* ### 测试部分
    基于已经给定的测试数据，通过程序结果和标准答案比对的方式，得到字正确率和句正确率

## 环境
程序编写与测试的环境为Visual Studio 2022，搭载的包有
* numpy
* json
* Counter
* re

## 安装
压缩包中按照如下格式：
```python
data/    input.txt    
         output.txt
src/     
         group_training.py #二元词组统计
         single_training.py #单个字统计
         viterbi.py #输出结果
         compare_output.py #比较测试输出和标准答案
#按照上述顺序运行这四个程序
readme 
```
**需要将训练的语料放入命名为‘training_set’的文件夹中，将文件夹放入src文件夹中。**

**需要将汉字拼音对照表命名为‘pinyin_table.txt’放置在src文件夹中。**

**将输入命名为‘std_input.txt’放入data文件夹，正确输出命名为‘std_output.txt’放入data文件夹，之后程序生成的输出将自动出现在data文件夹**





