import numpy as np
debug = False

updates=[]
with open('/home/pi/Desktop/log_update.txt') as f:
    # read all the lines until EOF
    data = f.readlines()
    for line in data:                      
        if '(UTC' in line :
            date=line.strip()
            module = []
            # print(date)
        elif '[pouvant' in line :
            module.append(line.strip().replace(u'\xa0', u' ')) # https://www.delftstack.com/howto/python/ways-to-remove-xa0-from-a-string-in-python/                 
        elif '===='  in line and module != []: # if updates detected
            # print(module)
            updates.append((date, module))
    updates.append((date, module))

# last update        
print(updates[-1][0])
print(updates[-1][1])
    
import pandas as pd
import dateparser
import locale
# in terminal: locale -a will show all the 
# set local to french
locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')# ; locale.getlocale()
# pd.to_datetime('mercredi 2 septembre 2020', format= '%A %d %B %Y, %H:%M:%S (UTC%z)')
# set back to english
# locale.setlocale(locale.LC_ALL, 'C.UTF-8'); locale.getlocale()
# pd.to_datetime('sunday 2 september 2020', format= '%A %d %B %Y')  # ok

data = pd.DataFrame(updates, columns=['date','updates'])
# numbers of items in updates
data['n_items']=data['updates'].apply(len)

data['Date'] = pd.to_datetime(data['date'], format= '%A %d %B %Y, %H:%M:%S (UTC%z)')
#data['Date']= data['date'].apply(lambda x: dateparser.parse(x))
# utc
data['Date'] = pd.to_datetime(data['Date'], utc=True)
# us/eastern
if debug: print('Heure USA\n',data['Date'].apply(lambda x: x.tz_convert('US/Eastern')))
#print('Heure USA\n',data['Date'].dt.tz_convert('US/Eastern'))
# paris
data['Date'] = data['Date'].dt.tz_convert('Europe/Paris')
if debug: print('Heure Paris\n',data)

print(data.tail())
print(data.iloc[-1])

if debug:
    d =13
    print()
    print(data['date'][d])
    #print(data['updates'][0])

    for k in range(len(data['updates'][d])):
        mod = data['updates'][d][k].split('/')[0]
        package = data['updates'][d][k].split('/')[1].split(' ')[0]
        ver = data['updates'][d][k].split('/')[1].split(' ')[1]
        print(mod, '\t',package,'\t', ver)

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10,8))
data_month = data.groupby(pd.Grouper(key='Date',freq='M'))['updates'].count()
if debug: print(data_month)

def plotting():
    #plt.bar(data_hour)
    data_month.plot.bar(rot=0)
    plt.title('updates by month')
    ax.set_xticklabels(data_month.index.month) 
    plt.show()

def make_columns(row):
    mod = []
    package = []
    ver = []
    for k in range(len(row)):
        mod.append(row[k].split('/')[0])
        package.append(row[k].split('/')[1].split(' ')[0])
        ver.append(row[k].split('/')[1].split(' ')[1])
        #print(mod, '\t',package,'\t', ver)
    return mod, package, ver
    #return pd.DataFrame({'mod': np.array((mod,ver))})
    #return pd.DataFrame([np.array(mod), np.array(package), np.array(ver)], columns=['items', 'packages','ver'])

if debug:
    # test one row
    d = 13
    test = make_columns(data['updates'][d])
    print('row',d,test)

df = data['updates'].apply(make_columns)
df2 = pd.DataFrame({'all': df})
# https://stackoverflow.com/questions/35491274/split-a-pandas-column-of-lists-into-multiple-columns
data[['module','source','version']] = pd.DataFrame(df2['all'].tolist()) #, index= df2.index)
# pd.DataFrame(df2["all"].to_list(), columns=['mod','package','ver'])
if debug:
    print(data['module'])

df3 = df2['all'].apply(pd.Series)
df3.columns = ['module', 'source','version']
if debug:
    print(df3)

# last updates
last = 2
print('Last',last,'updates')
data_module = pd.DataFrame(data.module.to_list())
print('Last update')
#print(data.tail(last).date)
print(data.tail(last).T)

# list of updated modules
all_mod = [[i for i in data_module[k]] for k in range(39)]
all_mod = np.array(all_mod).flatten()

# create dataframe
print('df_mod')
df_mod = pd.DataFrame(all_mod, columns=['updated_modules']).dropna()

# count occurences
occurs = df_mod.value_counts()

# counts() returns a multi-index pandas.Series
# convert multi-index to simple index
list_index= [x[0] for x in occurs.index]
occurs.index = list_index
#print(occurs)

def plotting1():
    # plot bar by ascending occurences
    thres = 2
    over5 = occurs[occurs>thres]
    over5.plot.barh(rot=0)
    #ax.set_xticklabels(over5.index)
    plt.yticks(fontsize=8) #, rotation=0)
    plt.tight_layout()
    plt.show()

    # plot bar by names
    over5.sort_index(ascending=False).plot.barh()
    #ax.set_xticklabels(over5.index)
    plt.yticks(fontsize=8, rotation=0)
    plt.tight_layout()
    plt.show()

# sources as lists in columns
# https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173
dataT = data.T
#source = np.array(dataT.loc['source']).flatten()
sources = data["source"].apply(pd.Series)

def to_1D(series):
    #return pd.Series([x if type(_list)==list else _list for _list in series for x in _list])
    return pd.Series([x for _list in series for x in _list])

def flatten(series):
    rt = []
    for i in series:
        if isinstance(i,list): rt.extend(flatten(i))
        else: rt.append(i)
    return rt

unique_items = to_1D(data["source"]).value_counts()
print('sources :\n',unique_items)

#print('testing')
all_sources = sources[0].dropna()
#print(all_sources)

testing_count = all_sources[all_sources=='testing'].count()

update_testing = sources[0][sources[0]=='testing'].count()
print('Pct of testing update', round(testing_count/len(all_sources)*100,2),'%')

#plotting()
#plotting1()


# list the last
# for loops
for k in list(updates[-1]):
        if type(k) != list:
            print(k)
        else:
            for j in k:
                print('\t',j)

# flatten
print()
for k in flatten(updates[-1]):
            print(k,'\n\t ',end='')

# translate, maketrans
print()
mytable=str(updates[-1]).maketrans("[]()'","     ")
split_list=str(updates[-1]).translate(mytable).split(' , ')
for k in split_list:
    print(k.strip(),'\n\t ',end='')