#importing the required libraries
import pickle
import csv
#opening the required files for merging .obj file contains the data collected through beautiful soap and .txt file contains the data of the poets and poems
with open ('poems.obj','rb') as b_soup, open ('collection.txt','r') as scrapped, open('data_merged.csv','w',newline='',encoding='utf-8') as merger :
    all_poems = []
    poet_titles = []
    # poets = []
    # titles = []
#running through each line of the text file and extracting the name of the poet, title of poem and the poem itself
    for l in scrapped:

        line = l.split(sep='~')
        temp = []
        poet = line[0].strip()
        year = ''
        title = line[2].strip()
        poem = line[3].strip()

        # if poet not in poets:
        #     poets.append(poet)
        
        temp.append(poet)
        poet_titles.append({poet,title})
        # if title not in titles:
        #     titles.append(title)
        
        #here we are extracting the year of the peom
        for i in line[1]:
            if i.isnumeric():
                year += c
        if len(year) > 4:
            year = year[-4:]
        temp.append(year)

        temp.append(title)
#now we try to classify the era of the peom based on the year it was composed
#if no year is given we do not add the era in the poem 
        if year == '':
            temp.append('')
        else:
            if int(year) > 1900:
                temp.append('आधुनिक काल')
            elif int(year) > 1700:
                temp.append('रीति काल')
            elif int(year) > 1375:
                temp.append('भक्ति काल')
            else:
                temp.append('आदिकाल')
# we are storing in each iteration we are storing the poet, year , title, era of poem and th poem itself in a tempp variable
        temp.append(poem)
# after storing all the required info in tempp variable we store the poem in poem variable
        all_poems.append(temp)
        # print(temp)
        # break
#extracting the data in the similar way from the .obj file
    data = pickle.load(b_soup)
    for line in data:

        temp =[]

        poet = line[0].strip()
        year = ''
        title = line[3].strip()
        
        poem = line[4].replace("\n","")
        poem = poem.strip()

        if {poet,title} in poet_titles:
            # print('here')
            continue

        
        
        temp.append(poet)
        
        for c in line[1]:
            if c.isnumeric():
                year += c
                
        if len(year) > 4:
            year = year[-4:]
        temp.append(year)

        temp.append(title)

        if year == '':
            temp.append('')
        else:
            if int(year) > 1900:
                temp.append('आधुनिक काल')
            elif int(year) > 1700:
                temp.append('रीति काल')
            elif int(year) > 1375:
                temp.append('भक्ति काल')
            else:
                temp.append('आदिकाल')

        temp.append(poem)
        all_poems.append(temp)
    
#writing all the rows of all_poems in the csv file 
    # for a in all_poems:
    #     merger.write(str(a) + '\n')
    writer = csv.writer(merger)
    writer.writerows(all_poems)
