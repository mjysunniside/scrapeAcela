import pandas as pd
from matplotlib import pyplot as plt



df = pd.read_csv('./result.csv')
print(df.keys())
with_owner = (
 df.groupby('Company', as_index=False)['STC Watts'].sum()
   .assign(percent=lambda d: d['STC Watts'].div(d['STC Watts'].sum())
                                           .mul(100).round(2)
           )
)

step_one = df.groupby('Company', as_index=False)['STC Watts'].sum()
step_one.drop(step_one[step_one['Company'] == "OWNER"].index, inplace = True)
no_owner = step_one.assign(percent=lambda d: d['STC Watts'].div(d['STC Watts'].sum())
                                           .mul(100).round(2)
           )
print(no_owner)




# df['Company'].value_counts()['Cal Solar']

finaled_permits = df.groupby(['Finaled Date']).get_group('Finaled')

total_finaled_count = len(finaled_permits.index)
finaled_value_counts = finaled_permits['Company'].value_counts()

# print(finaled_permits['Company'].value_counts())

no_owner_value_counts = finaled_value_counts.drop('OWNER')
no_owner_total = no_owner_value_counts.sum()
keys = no_owner_value_counts.keys()

# exit()

porcent = 100.*no_owner_value_counts/no_owner_total

patches, texts = plt.pie(no_owner_value_counts, startangle=90, radius=1.2)
labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(keys, porcent)]

sort_legend = True
if sort_legend:
    patches, labels, dummy =  zip(*sorted(zip(patches, labels, no_owner_value_counts),
                                          key=lambda x: x[2],
                                          reverse=True))

plt.legend(patches, labels, loc='center left', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)

plt.savefig('piechart.png', bbox_inches='tight')

