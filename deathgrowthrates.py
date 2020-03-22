import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


font = {'family': 'normal',
        # 'weight': 'bold',
        'size': 16}

matplotlib.rc('font', **font)

plt.style.use('bmh')

path = 'data/csse_covid_19_data/csse_covid_19_time_series/' +\
       'time_series_19-covid-{}.csv'
confirmed = pd.read_csv(path.format('Confirmed'))
deaths = pd.read_csv(path.format('Deaths'))
recovered = pd.read_csv(path.format('Recovered'))

# checking for the growth of deaths and whether it phases out
# by examining the slope in the logarithmic plot
# mycountryl = ['Austria', 'Switzerland', 'US',
#               'United Kingdom', 'Korea, South']
mycountryl = ['Germany', 'Spain', 'Italy', 'France', 'China', 'US',
              'Switzerland', 'Korea, South']
ncs = len(mycountryl)
dtwo = deaths.copy()
dtwo.drop(columns=['Province/State', 'Lat', 'Long'], inplace=True)
cfig = plt.figure(100, figsize=(16, 12), dpi=100)
for idx, mycountry in enumerate(mycountryl):
    ax = cfig.add_subplot(3, 3, idx+1)
    mcdtwo = dtwo[dtwo['Country/Region'] == mycountry]
    # sick of pandas? -- convert the data frame to a numpy array
    gdl = mcdtwo.values.tolist()
    # only the numerical values
    gda = np.array(gdl[0][1:])
    # take the log of them
    lggda = np.log2(gda)
    # set the infs to zero
    lggda[np.isneginf(lggda)] = 0
    # the slope is the difference
    slopes = lggda[1:] - lggda[:-1]
    # use an average
    avgslopes = .5*(slopes[1:] + slopes[:-1])
    fivedaysavrg = .2*(slopes[:-4] + slopes[1:-3] + slopes[2:-2]
                       + slopes[3:-1] + slopes[4:])
    fdl = fivedaysavrg.tolist()
    # extend with NaN to align with the data in the plots
    nfdl = [np.NaN, np.NaN]
    nfdl.extend(fdl)
    nfdl.extend([np.NaN, np.NaN])
    ax.plot(slopes[-50:], 'o', label='daily value')
    ax.plot(avgslopes[-50:], 'o', label='two days average')
    ax.plot(nfdl[-50:], label='five days average')
    if not (mycountry == 'China'):  # or mycountry == 'Korea, South'):
        ax.set_ylim(ymin=-.05, ymax=1.)
    ax.set_title(mycountry)
ax = cfig.add_subplot(3, 3, idx+2)
ax.plot(np.NaN, 'o', label='daily value')
ax.plot(np.NaN, 'o', label='two days average')
ax.plot(np.NaN, label='five days average')
ax.axis('off')
ax.legend(loc='center')
plt.tight_layout()
plt.savefig('slopes-dsifc.png')
plt.savefig('slopes-dsifc.pdf')


def getthelogslope(npa):
    lggda = np.log2(npa)
    # set the infs to zero
    lggda[np.isneginf(lggda)] = 0
    # the slope is the difference
    slopes = lggda[1:] - lggda[:-1]
    # use an average
    avgslopes = .5*(slopes[1:] + slopes[:-1])
    fivedaysavrg = .2*(slopes[:-4] + slopes[1:-3] + slopes[2:-2]
                       + slopes[3:-1] + slopes[4:])
    fdl = fivedaysavrg.tolist()
    # extend with NaN to align with the data in the plots
    nfdl = [np.NaN, np.NaN]
    nfdl.extend(fdl)
    nfdl.extend([np.NaN, np.NaN])
    return slopes, avgslopes, fivedaysavrg


# ## The plots of the example scenarios
N = 80
expgrwth = np.array([1.1**x for x in range(N)])
expgrwthl = []
for x in range(N):
    expgrwthl.append(expgrwth[:x].sum())
xpgslp, _, _ = getthelogslope(10+np.array(expgrwthl))
lingrwth = np.array([100+10*x for x in range(N)])
lngslp, _, _ = getthelogslope(lingrwth)
expdecay = np.exp(-.1*np.arange(N))
exdgrwth = []
for x in range(N):
    exdgrwth.append(1000+100*expdecay[:x].sum())
exdgrwth = np.array(exdgrwth)
edslp, _, _ = getthelogslope(exdgrwth)
plt.figure(2, figsize=(8, 4), dpi=100)
plt.plot(xpgslp, 'o', label='exp growth')
plt.plot(lngslp, 'o', label='constant growth')
plt.plot(edslp, 'o', label='decaying growth')
plt.title('Example Scenarios')
plt.legend()
plt.savefig('slopes-examples.png')
plt.savefig('slopes-examples.pdf')
# plt.show()

cfig = plt.figure(3, figsize=(8, 4), dpi=100)
ax = cfig.add_subplot(1, 1, 1)
covidsimdata = pd.read_csv('CovidSIM-results-1.csv')
covidsimdatanoi = pd.read_csv('CovidSIM-results-2.csv')
deaths = covidsimdata[' Deaths'].values
deathsnoi = covidsimdatanoi[' Deaths'].values
covisim, _, _ = getthelogslope(deaths)
covisimnoi, _, _ = getthelogslope(deathsnoi)
ax.plot(covisimnoi, 'o', label='Scenario without intervention')
ax.plot(covisim, 'o', label='Scenario with max ICU < 45,000')

ax.set_ylim(ymin=-.05, ymax=1.)
ax.legend()
ax.set_title('Simulated Scenarios for Germany')
plt.savefig('slopes-simulation.png')
plt.savefig('slopes-simulation.pdf')

plt.show()
