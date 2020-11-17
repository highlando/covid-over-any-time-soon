import numpy as np
import matplotlib.pyplot as plt
import datetime

plt.style.use('bmh')
alphas = [.05*x for x in range(10)]

now = datetime.datetime.now()
today = 'as of {0}. '.format(now.day) + now.strftime("%B")


def getthelogslope(npa):
    lggda = np.log2(npa)
    # set the infs to zero
    lggda[np.isneginf(lggda)] = 0
    # the slope is the difference
    slopes = lggda[1:] - lggda[:-1]
    # use an average
    avgslopes = .5*(slopes[1:] + slopes[:-1])
    svndaysavrg = 1/7*(slopes[:-6] + slopes[1:-5] + slopes[2:-4]
                       + slopes[3:-3] + slopes[4:-2] + slopes[5:-1]
                       + slopes[6:])
    # fdl = svndaysavrg.tolist()
    # extend with NaN to align with the data in the plots
    # nfdl = [np.NaN, np.NaN]
    # nfdl.extend(fdl)
    # nfdl.extend([np.NaN, np.NaN])
    return slopes, avgslopes, svndaysavrg


def getthepercincreases(npa):
    # set the infs to zero
    # the slope is the difference
    slopes = (npa[1:] - npa[:-1])/npa[:-1]*100
    # use an average
    avgslopes = .5*(slopes[1:] + slopes[:-1])
    # fivedaysavrg = .2*(slopes[:-4] + slopes[1:-3] + slopes[2:-2]
    #                    + slopes[3:-1] + slopes[4:])
    svndaysavrg = 1/7*(slopes[:-6] + slopes[1:-5] + slopes[2:-4]
                       + slopes[3:-3] + slopes[4:-2] + slopes[5:-1]
                       + slopes[6:])
    fdl = svndaysavrg.tolist()
    # extend with NaN to align with the data in the plots
    nfdl = [np.NaN]*6
    nfdl.extend(fdl)
    return slopes, avgslopes, np.array(nfdl)


def getxranges(datarray, init=1000, factor=3):
    idxl = []
    cmrgn = init
    while datarray[-1] > cmrgn:
        idxl.append((datarray < cmrgn).sum())
        cmrgn = cmrgn*factor
    return idxl


def plotlogslops(pddf, countryl, ncols=3, fignum=100, dpi=100,
                 ndays=100, plotdays=90, figfile=None):
    ncnt = len(countryl)
    nrows = np.int(np.ceil(ncnt/ncols))
    cfig = plt.figure(fignum, figsize=(5*ncols, 4*nrows), dpi=dpi)
    for idx, mycountry in enumerate(countryl):
        ax = cfig.add_subplot(nrows, ncols, idx+1)
        mcdtwo = pddf[pddf['Country/Region'] == mycountry]
        # sick of pandas? -- convert the data frame to a numpy array
        gdl = mcdtwo.values.tolist()
        # only the numerical values
        gda = np.array(gdl[0][2:])
        # take the log of them
        for gdll in gdl[1:]:  # sum up if there are more regions per country
            gda = gda + np.array(gdll[2:])

        ggda = gda[-ndays:] - gda[-ndays-1]
        # slopes, tdavrg, fdavrg = getthelogslope(ggda)
        slopes, tdavrg, fdavrg = getthepercincreases(ggda)
        ax.plot(slopes[-plotdays:], 'o', label='daily value')
        ax.plot(tdavrg[-plotdays:], 'o', label='two days average')
        ax.plot(fdavrg[-plotdays:], label='seven days average')

        ax.set_xlim(xmin=-2.45, xmax=plotdays+2.45)
        # ymax, ymin = .315, -.015
        ymax, ymin = 11, -1
        ax.set_ylim(ymin=ymin, ymax=ymax)

        xranges = getxranges(ggda[-ndays:], init=1000, factor=3)
        xranges.append(ndays+1)
        lstxmin = 0
        for kk, xrng in enumerate(xranges):
            if xrng == ndays+1:
                xmax = 1
            else:
                xmax = .975*(xrng-1)/ndays
            # plt.axhspan(-.05, ymax, xmin=lstxmin, xmax=xmax,
            #             alpha=alphas[kk])
            plt.axhspan(-1, ymax, xmin=lstxmin, xmax=xmax, alpha=alphas[kk])
            lstxmin = xmax

        if idx >= (nrows-1)*ncols:
            ax.set_xlabel('the last {0} days'.format(plotdays))
        if np.mod(idx+1, ncols) == 0:
            ax.set_ylabel('daily plus [%]')
            ax.yaxis.set_label_position("right")

        ax.text(.8, .8, '{0:d}'.format(np.int(ggda[-1])),
                transform=ax.transAxes,
                bbox={'facecolor': 'white', 'alpha': .5})
        ax.set_title(mycountry)
    ax = cfig.add_subplot(nrows, ncols, idx+2)
    ax.plot([1, ndays], [8, 0], 'o', label='daily value')
    ax.plot([1, ndays], [6, 2], 'o', label='two days average')
    ax.plot([1, ndays], [7, 1], label='seven days average')
    ax.plot(np.NaN, '.', label=today)
    # ymax, ymin = .525, -.025
    ymax, ymin = 9, -1
    ax.set_ylim(ymin=ymin, ymax=ymax)
    # ax.axis('off')
    ax.legend(loc='center', facecolor='white')
    ax.set_xlabel('the last {0} days'.format(plotdays))
    ax.set_ylabel('daily plus [%]')
    ax.yaxis.set_label_position("right")
    # plt.axhspan(-.025, .525, xmin=0.275, xmax=.45, alpha=.05)
    # plt.axhspan(-.025, .525, xmin=0.45, xmax=.615, alpha=.1)
    # plt.axhspan(-.025, .525, xmin=0.615, xmax=.8, alpha=.15)
    # plt.axhspan(-.025, .525, xmin=0.8, xmax=1., alpha=.2)
    plt.axhspan(-1, 11, xmin=0.275, xmax=.45, alpha=.05)
    plt.axhspan(-1, 11, xmin=0.45, xmax=.615, alpha=.1)
    plt.axhspan(-1, 11, xmin=0.615, xmax=.8, alpha=.15)
    plt.axhspan(-1, 11, xmin=0.8, xmax=1., alpha=.2)
    bbstl = {'facecolor': 'white', 'alpha': .5}
    ax.text(.6, .8, 'total cases', transform=ax.transAxes,
            bbox=bbstl)
    ax.text(1, 0.02, '<1000 \n    cases', bbox=bbstl)
    ax.text(14/50*ndays, 0.07, '>1000', bbox=bbstl)
    ax.text(24/50*ndays, 0.07, '>3000', bbox=bbstl)
    ax.text(33/50*ndays, 0.07, '>9000', bbox=bbstl)
    ax.text(43/50*ndays, 0.07, '>27000', bbox=bbstl)
    ax.set_title('Legend')
    plt.tight_layout()
    if figfile is not None:
        plt.savefig(figfile)
    return cfig


def lmonthslops(pddf, countryl, ncols=3, fignum=100, dpi=100,
                ndays=40, plotdays=30, figfile=None):
    ncnt = len(countryl)
    nrows = np.int(np.ceil(ncnt/ncols))
    cfig = plt.figure(fignum, figsize=(5*ncols, 4*nrows), dpi=dpi)
    for idx, mycountry in enumerate(countryl):
        ax = cfig.add_subplot(nrows, ncols, idx+1)
        mcdtwo = pddf[pddf['Country/Region'] == mycountry]
        # sick of pandas? -- convert the data frame to a numpy array
        gdl = mcdtwo.values.tolist()
        # only the numerical values
        gda = np.array(gdl[0][2:])
        for gdll in gdl[1:]:  # sum up if there are more regions per country
            gda = gda + np.array(gdll[2:])

        ggda = gda[-ndays:] - gda[-ndays-1]
        slopes, tdavrg, fdavrg = getthepercincreases(ggda)
        ax.plot(slopes[-plotdays:], 'o', label='daily value')
        ax.plot(tdavrg[-plotdays:], 'o', label='two days average')
        ax.plot(fdavrg[-plotdays:], label='seven days average')

        ax.set_xlim(xmin=-2.45, xmax=plotdays+2.45)
        ymax, ymin = 11, -1
        ax.set_ylim(ymin=ymin, ymax=ymax)
        ax.set_yticks([0, 5, 10])

        if idx >= (nrows-1)*ncols:
            ax.set_xlabel('the last {0} days'.format(plotdays))
        if np.mod(idx+1, ncols) == 0:
            ax.set_ylabel('daily plus [%]')
            ax.yaxis.set_label_position("right")

        ax.text(.8, .8, '{0:d}'.format(np.int(gda[-1]-gda[-plotdays-1])),
                transform=ax.transAxes,
                bbox={'facecolor': 'white', 'alpha': .5})
        ax.set_title(mycountry)
    ax = cfig.add_subplot(nrows, ncols, idx+2)
    # ax.plot([1, plotdays], [.5, 0], 'o', label='daily value')
    # ax.plot([1, plotdays], [.45, .05], 'o', label='two days average')
    # ax.plot([1, plotdays], [.475, .025], label='five days average')
    ax.plot([1, ndays], [8, 0], 'o', label='daily value')
    ax.plot([1, ndays], [6, 2], 'o', label='two days average')
    ax.plot([1, ndays], [7, 1], label='seven days average')
    ax.plot(np.NaN, '.', label=today)
    # ymax, ymin = .525, -.025
    ymax, ymin = 9, -1
    ax.set_ylim(ymin=ymin, ymax=ymax)
    # ax.axis('off')
    ax.legend(loc='center', facecolor='white')
    ax.set_xlabel('the last {0} days'.format(plotdays))
    ax.set_ylabel('daily plus [%]')
    ax.yaxis.set_label_position("right")
    bbstl = {'facecolor': 'white', 'alpha': .5}
    ax.text(.375, .8, 'last month cases', transform=ax.transAxes,
            bbox=bbstl)
    ax.set_title('Legend')
    plt.tight_layout()
    if figfile is not None:
        plt.savefig(figfile)
    return cfig


if __name__ == '__main__':
    tstdta = np.array([10*1.2**x for x in range(50)])
    tstdtamax = np.max(tstdta)
    plt.figure()
    plt.plot(tstdta)
    xranges = getxranges(tstdta)
    lstxmin = 0
    for kk, xrng in enumerate(xranges):
        xmax = xrng/(tstdta.size-1)
        print(alphas[kk])
        plt.axhspan(-.05, tstdtamax, xmin=lstxmin, xmax=xmax, alpha=alphas[kk])
        lstxmin = xmax
    plt.show()
