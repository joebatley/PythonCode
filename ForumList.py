

from random import randint
import numpy
Dict = {1:'Mark Elkin',
2:'Ales Hrabec',
3:'Jangyong Kim',
4:'Nick Porter',
5:'James Witt',
6:'Joe Batley',
7:'Robert Buda',
8:'Fatma Al MaMari',
9:'Scott Marmion',
10:'Arpita Mitra',
11:'Tim Moorsom',
12:'Sophie Morley',
13:'Nathan Satchell',
14:'Philippa Shepley',
15:'Dong Shi',
16:'Priyasmita Sinha',
17:'Charles Spencer',
18:'Georgios Stefanou',
19:'Rowan Temple',
20:'Adam Wells',
21:'Amy Westerman',
22:'May Wheeler'}

done = []
 
for i in range(len(Dict.keys())/2):
    a = randint(1,22)
    
    while a in done:
        if a in done:
            a=randint(1,22)    
    done.append(a)
    
    
    b =  randint(1,22)
    while b in done:
        if b in done:
            b=randint(1,22)    
    done.append(b)
    
    print Dict[a] + ' and ' + Dict[b]    
        
print numpy.sort(done)