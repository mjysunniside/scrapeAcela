import pandas as pd
from matplotlib import pyplot as plt


def makePlot():
    df = pd.read_csv('./result.csv')
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
    # print(no_owner)
    #plotting now
    patches, texts = plt.pie(no_owner['percent'], startangle=90, radius=1.2)
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(no_owner['Company'], no_owner['percent'])]

    sort_legend = True
    if sort_legend:
        patches, labels, dummy =  zip(*sorted(zip(patches, labels, no_owner['percent']),
                                            key=lambda x: x[2],
                                            reverse=True))

    plt.legend(patches, labels, loc='center left', bbox_to_anchor=(-0.1, 1.),
            fontsize=8)

    plt.savefig('piechart2.png', bbox_inches='tight')

