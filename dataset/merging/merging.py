import pickle
import csv
with open ('poems (1).obj','rb') as fin, open ('collection.txt','r') as fin2, open('data_merged.csv','w',newline='',encoding='utf-8') as fout :
    poems = []
    poet_titles = []
    # poets = []
    # titles = []

    for l in fin2:

        line = l.split(sep='~')
        tem = []
        
        poet = line[0].strip()
        year = ''
        title = line[2].strip()
        poem = line[3].strip()

        # if poet not in poets:
        #     poets.append(poet)
        
        tem.append(poet)
        poet_titles.append({poet,title})
        # if title not in titles:
        #     titles.append(title)
        
        for c in line[1]:
            if c.isnumeric():
                year += c
        if len(year) > 4:
            year = year[-4:]
        tem.append(year)

        tem.append(title)

        if year == '':
            tem.append('')
        else:
            if int(year) > 1900:
                tem.append('आधुनिक काल')
            elif int(year) > 1700:
                tem.append('रीति काल')
            elif int(year) > 1375:
                tem.append('भक्ति काल')
            else:
                tem.append('आदिकाल')

        tem.append(poem)
        poems.append(tem)
        # print(tem)
        # break

    data = pickle.load(fin)
    for line in data:

        tem =[]

        poet = line[0].strip()
        year = ''
        title = line[3].strip()
        
        poem = line[4].replace("\n","")
        poem = poem.strip()

        if {poet,title} in poet_titles:
            # print('here')
            continue

        
        
        tem.append(poet)
        
        for c in line[1]:
            if c.isnumeric():
                year += c
                
        if len(year) > 4:
            year = year[-4:]
        tem.append(year)

        tem.append(title)

        if year == '':
            tem.append('')
        else:
            if int(year) > 1900:
                tem.append('आधुनिक काल')
            elif int(year) > 1700:
                tem.append('रीति काल')
            elif int(year) > 1375:
                tem.append('भक्ति काल')
            else:
                tem.append('आदिकाल')

        tem.append(poem)
        poems.append(tem)
    

    # for a in poems:
    #     fout.write(str(a) + '\n')
    writer = csv.writer(fout)
    writer.writerows(poems)
