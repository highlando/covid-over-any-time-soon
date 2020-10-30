import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from ghc_helpers import plotlogslops, getthelogslope, lmonthslops
from ghc_helpers import getthepercincreases

font = {'family': 'normal',
        # 'weight': 'bold',
        'size': 16}
ndays = 90

matplotlib.rc('font', **font)

plt.style.use('bmh')

pathd = 'data/csse_covid_19_data/csse_covid_19_time_series/' +\
        'time_series_covid19_deaths_global.csv'
pathc = 'data/csse_covid_19_data/csse_covid_19_time_series/' +\
        'time_series_covid19_confirmed_global.csv'
deaths = pd.read_csv(pathd)

somecntrl = ['Argentina', 'Australia', 'Austria',
             'Brazil', 'China', 'Croatia',
             'Denmark', 'Egypt', 'Greece',
             'India', 'Netherlands', 'Russia',
             'Switzerland', 'United Kingdom']

tworands = np.random.randint(0, 14, (2, ))
guestone = somecntrl[tworands[0]]
guesttwo = somecntrl[tworands[1]]
# guestthree = somecntrl[tworands[2]]

mycountryl = ['Germany', 'Spain', 'Italy', 'France', 'Sweden', 'US']

somecntrl.extend(mycountryl)
somecntrl.sort()
# mycountryl.extend([guestone, guesttwo, guestthree])
mycountryl.extend([guestone, guesttwo])

dtwo = deaths.copy()
dtwo.drop(columns=['Lat', 'Long'], inplace=True)
cfig = plotlogslops(dtwo, mycountryl, figfile='slopes-dsifc.png', ndays=ndays)
ccfig = plotlogslops(dtwo, somecntrl, fignum=200,
                     figfile='slopes-dsifc.pdf', ndays=ndays)

cfig = lmonthslops(dtwo, mycountryl, fignum=220,
                   figfile='lmslps-dsifc.png', ndays=50)
ccfig = lmonthslops(dtwo, somecntrl, fignum=230,
                    figfile='lmslps-dsifc.pdf', ndays=50)
# plt.show()

# ## The plots of the example scenarios
N = 80
expgrwth = np.array([1.1**x for x in range(N)])
expgrwthl = []
for x in range(N):
    expgrwthl.append(expgrwth[:x].sum())
xpgslp, _, _ = getthepercincreases(10+np.array(expgrwthl))
xpgslp, _, _ = getthepercincreases(10+np.array(expgrwthl))
lingrwth = np.array([100+10*x for x in range(N)])
lngslp, _, _ = getthepercincreases(lingrwth)
expdecay = np.exp(-.1*np.arange(N))
exdgrwth = []
for x in range(N):
    exdgrwth.append(1000+100*expdecay[:x].sum())
exdgrwth = np.array(exdgrwth)
edslp, _, _ = getthepercincreases(exdgrwth)
cfig = plt.figure(2, figsize=(8, 4), dpi=100)
ax = cfig.add_subplot(1, 1, 1)
ax.plot(xpgslp, 'o', label='exponential growth')
ax.plot(lngslp, 'o', label='constant growth')
ax.plot(edslp, 'o', label='decaying growth')
ax.set_title('Example Scenarios')
ax.set_ylabel('daily plus [%]')
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
covisim, _, _ = getthepercincreases(deaths)
covisimnoi, _, _ = getthepercincreases(deathsnoi)

icus = covidsimdata[' ICU'].values
icusnoi = covidsimdatanoi[' ICU'].values

ax.plot(covisimnoi, 'o', label='Scenario without intervention')
ax.plot(covisim, 'o', label='Scenario with max ICU < 45,000')
# ax.set_ylim(ymin=-.05, ymax=.5)
ax.set_ylim(ymin=-1, ymax=9)
ax.legend(facecolor='white')
ax.set_title('Simulated Slopes for Germany')
ax.set_ylabel('daily plus [%]')
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

plt.show()
