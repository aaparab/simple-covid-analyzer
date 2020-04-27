# Main 

import os, sys
from functions import *

datapath = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'data')

if __name__ == '__main__':
    
    # Illinois state (default)
    state = 'Illinois'
    filename = 'illinois_25apr.png'

    cdf = fetch_data()    # cases data
    cdf = slice_fit(cdf)

    ddf = fetch_data(cases_data=False)    # deaths data
    ddf = slice_fit(ddf)

    plot(deathdf=ddf, casedf=cdf, saveloc=os.path.join(datapath, filename))

    # California state
    state = 'California'
    filename = 'cali_25apr.png'

    cdf = fetch_data()
    cdf = slice_fit(cdf, state=state, polydeg=8)
    plot(casedf=cdf, state=state, saveloc=os.path.join(datapath, filename))

    print('Program completed successfully.')
