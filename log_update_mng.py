import numpy as np

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
print('Heure USA\n',data['Date'].apply(lambda x: x.tz_convert('US/Eastern')))
#print('Heure USA\n',data['Date'].dt.tz_convert('US/Eastern'))
# paris
data['Date'] = data['Date'].dt.tz_convert('Europe/Paris')
print('Heure Paris\n',data)


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
print(data_month)
#plt.bar(data_hour)
data_month.plot.bar(rot=0)
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

# test one row
test = make_columns(data['updates'][d])
print('row',d,test)

df = data['updates'].apply(make_columns)
df2 = pd.DataFrame({'all': df})
# https://stackoverflow.com/questions/35491274/split-a-pandas-column-of-lists-into-multiple-columns
data[['module','source','version']] = pd.DataFrame(df2['all'].tolist(), index= df2.index)
# pd.DataFrame(df2["all"].to_list(), columns=['mod','package','ver'])
print(data['module'])

df3 = df2['all'].apply(pd.Series)
df3.columns = ['module', 'source','version']
print(df3)

data_module = pd.DataFrame(data.module.to_list())

all_mod = [[i for i in data_module[k]] for k in range(39)]
all_mod = np.array(all_mod).flatten()

df4 = pd.DataFrame(all_mod)
occurs = df4.value_counts()
print(occurs)

thres = 2
over5 = occurs[occurs>thres]
over5.plot.barh(rot=0)
#ax.set_xticklabels(over5.index)
plt.yticks(fontsize=8) #, rotation=0)
plt.tight_layout()
plt.show()

over5.sort_index(ascending=False).plot.barh()
#ax.set_xticklabels(over5.index)
plt.yticks(fontsize=8, rotation=0)
plt.tight_layout()
plt.show()