import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import datetime


font = {'family': 'normal',
        # 'weight': 'bold',
        'size': 16}

matplotlib.rc('font', **font)

plt.style.use('bmh')

path = 'data/csse_covid_19_data/csse_covid_19_time_series/' +\
       'time_series_covid19_deaths_global.csv'
deaths = pd.read_csv(path)

now = datetime.datetime.now()
today = 'as of {0}. '.format(now.day) + now.strftime("%B")

# checking for the growth of deaths and whether it phases out
# by examining the slope in the logarithmic plot
# mycountryl = ['Austria', 'Switzerland', 'US',
#               'United Kingdom', 'Korea, South']
somecntrl = ['Austria', 'Brazil', 'Croatia',
             'Denmark', 'Egypt', 'India',
             'Korea, South', 'Netherlands', 'Russia',
             'Sweden', 'Switzerland', 'United Kingdom']

tworands = np.random.randint(0, 10, (2, ))
guestone = somecntrl[tworands[0]]
guesttwo = somecntrl[tworands[1]]

mycountryl = ['Germany', 'Spain', 'Italy', 'France', 'China', 'US',
              guestone, guesttwo]

ncs = len(mycountryl)
dtwo = deaths.copy()
dtwo.drop(columns=['Lat', 'Long'], inplace=True)
cfig = plt.figure(100, figsize=(16, 12), dpi=100)
for idx, mycountry in enumerate(mycountryl):
    ax = cfig.add_subplot(3, 3, idx+1)
    mcdtwo = dtwo[dtwo['Country/Region'] == mycountry]
    # sick of pandas? -- convert the data frame to a numpy array
    gdl = mcdtwo.values.tolist()
    # only the numerical values
    gda = np.array(gdl[0][2:])
    # take the log of them
    for gdll in gdl[1:]:  # sum up if there are more regions per country
        gda = gda + np.array(gdll[2:])
    # if mycountry == 'China':
    #     import ipdb
    #     ipdb.set_trace()

    lggda = np.log2(gda)
    # set the infs to zero
    lggda[np.isneginf(lggda)] = np.NaN
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
    ax.set_xlim(xmin=-2.45, xmax=52.45)
    if not (mycountry == 'China'):  # or mycountry == 'Korea, South'):
        ax.set_ylim(ymin=-.05, ymax=1.)
    if idx == 6 or idx == 7:
        ax.set_xlabel('the last 50 days')
    if idx == 2 or idx == 5:
        ax.set_ylabel('slopes in casualties')
        ax.yaxis.set_label_position("right")
    ax.set_title(mycountry)
ax = cfig.add_subplot(3, 3, idx+2)
ax.plot([1, 50], [1, 0], 'o', label='daily value')
ax.plot([1, 50], [.9, .1], 'o', label='two days average')
ax.plot([1, 50], [.95, .05], label='five days average')
ax.plot(np.NaN, '.', label=today)
# ax.axis('off')
ax.legend(loc='center', facecolor='white')
ax.set_xlabel('the last 50 days')
ax.set_ylabel('slopes in casualties')
ax.yaxis.set_label_position("right")
ax.set_title('Legend')
plt.tight_layout()
plt.savefig('slopes-dsifc.png')
# plt.savefig('slopes-dsifc.pdf')

# # all countries as pdf
mycountryl.extend(somecntrl)
cfig = plt.figure(101, figsize=(16, 28), dpi=100)
for idx, mycountry in enumerate(mycountryl):
    ax = cfig.add_subplot(7, 3, idx+1)
    mcdtwo = dtwo[dtwo['Country/Region'] == mycountry]
    # sick of pandas? -- convert the data frame to a numpy array
    gdl = mcdtwo.values.tolist()
    # only the numerical values
    gda = np.array(gdl[0][2:])
    # take the log of them
    for gdll in gdl[1:]:  # sum up if there are more regions per country
        gda = gda + np.array(gdll[2:])
    # if mycountry == 'China':
    #     import ipdb
    #     ipdb.set_trace()

    lggda = np.log2(gda)
    # set the infs to zero
    lggda[np.isneginf(lggda)] = np.NaN
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
    ax.set_xlim(xmin=-2.45, xmax=52.45)
    if not (mycountry == 'China'):  # or mycountry == 'Korea, South'):
        ax.set_ylim(ymin=-.05, ymax=1.)
    if idx == 18 or idx == 19:
        ax.set_xlabel('the last 50 days')
    if idx == 2 or idx == 5 or idx == 8 or idx == 11 or idx == 14 or idx == 17:
        ax.set_ylabel('slopes in casualties')
        ax.yaxis.set_label_position("right")
    ax.set_title(mycountry)
ax = cfig.add_subplot(7, 3, idx+2)
ax.plot([1, 50], [1, 0], 'o', label='daily value')
ax.plot([1, 50], [.9, .1], 'o', label='two days average')
ax.plot([1, 50], [.95, .05], label='five days average')
ax.plot(np.NaN, '.', label=today)
# ax.axis('off')
ax.legend(loc='center', facecolor='white')
ax.set_xlabel('the last 50 days')
ax.set_ylabel('slopes in casualties')
ax.yaxis.set_label_position("right")
ax.set_title('Legend')
plt.tight_layout()
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
cfig = plt.figure(2, figsize=(8, 4), dpi=100)
ax = cfig.add_subplot(1, 1, 1)
ax.plot(xpgslp, 'o', label='exponential growth')
ax.plot(lngslp, 'o', label='constant growth')
ax.plot(edslp, 'o', label='decaying growth')
ax.set_title('Example Scenarios')
ax.set_ylabel('slopes in casualties')
ax.set_xlabel('days of simulation')
ax.yaxis.set_label_position("right")
plt.tight_layout()
plt.legend(facecolor='white')
plt.savefig('slopes-examples.png')
# plt.savefig('slopes-examples.pdf')
# plt.show()

cfig = plt.figure(3, figsize=(8, 8), dpi=100)
ax = cfig.add_subplot(2, 1, 1)
covidsimdata = pd.read_csv('CovidSIM-results-1.csv')
covidsimdatanoi = pd.read_csv('CovidSIM-results-2.csv')
deaths = covidsimdata[' Deaths'].values
deathsnoi = covidsimdatanoi[' Deaths'].values
covisim, _, _ = getthelogslope(deaths)
covisimnoi, _, _ = getthelogslope(deathsnoi)

icus = covidsimdata[' ICU'].values
icusnoi = covidsimdatanoi[' ICU'].values

ax.plot(covisimnoi, 'o', label='Scenario without intervention')
ax.plot(covisim, 'o', label='Scenario with max ICU < 45,000')
ax.set_ylim(ymin=-.05, ymax=1.)
ax.legend(facecolor='white')
ax.set_title('Simulated Slopes for Germany')
ax.set_ylabel('slopes in casualties')
ax.yaxis.set_label_position("right")
ax.set_xlabel('days of simulation')

# plt.tight_layout()
# plt.savefig('slopes-simulation.png')
# plt.savefig('slopes-simulation.pdf')

# cfig = plt.figure(4, figsize=(8, 4), dpi=100)
ax = cfig.add_subplot(2, 1, 2)
ax.plot(icusnoi, 'o', label='Scenario without intervention')
ax.plot(icus, 'o', label='Scenario with max ICU < 45,000')
ax.legend(facecolor='white')
ax.set_ylabel('people needing intensive care')
ax.yaxis.set_label_position("right")
ax.set_xlabel('days of simulation')
ax.set_title('Corresponding Need for ICUs')
plt.tight_layout()
plt.savefig('slopes-icus-simulation.png')
# plt.savefig('slopes-icus-simulation.pdf')

# plt.show()
