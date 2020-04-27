# List of functions

def fetch_data(cases_data=True, startdate=None):
    """Fetches US COVID dataset"""
    
    import pandas as pd
    
    caseurl = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/us_confirmed.csv'
    deathurl = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/us_deaths.csv'
    if cases_data is True:
        _df = pd.read_csv(caseurl)
    else:
        _df = pd.read_csv(deathurl)
    _df.columns = [col.lower() for col in _df.columns]
    _df.date = pd.to_datetime(_df.date)
    
    if startdate is not None:
        _df = _df.loc[_df.date > startdate]

    return _df

def slice_fit(df, state='Illinois', polydeg=6):
    """Slices data by state and fits a polynomial. """
    
    import numpy.polynomial.polynomial as poly

    _df = df.copy()
    _df = _df.loc[_df['province/state'] == state, ['date', 'case']].\
            groupby('date').sum()
    _df['_diff'] = _df.case.diff().fillna(0).astype('uint')
    
    # fit polynomial to "case"
    _coeffs = poly.polyfit(x=list(range(len(_df))), y=_df.case, deg=polydeg)
    _fitvals = poly.polyval(x=list(range(len(_df))), c=_coeffs)
    _df['_fitvals_case'] = _fitvals
    
    # fit polynomial to "_diff"
    _coeffs = poly.polyfit(x=list(range(len(_df))), y=_df._diff, deg=polydeg)
    _fitvals = poly.polyval(x=list(range(len(_df))), c=_coeffs)
    _df['_fitvals_diff'] = _fitvals
    
    return _df

def plot(casedf=None, deathdf=None, fit=True, state='Illinois', cumulative=False, saveloc=None):
    """Plots dataset."""
    
    import matplotlib.pyplot as plt
    
    if casedf is None:
        if deathdf is None:
            return None
        else:
            ylabel1 = 'Deaths per day'
            df1 = deathdf
            nrows = 1
            ylen = 5
            stitle = 'COVID-19 deaths in {}'.format(state)
    elif deathdf is None:
        ylabel1 = 'Cases per day'
        df1 = casedf
        nrows = 1
        ylen = 5
        stitle = 'COVID-19 cases in {}'.format(state)
    else:
        ylabel1 = 'Cases per day'
        ylabel2 = 'Deaths per day'
        df1 = casedf
        df2 = deathdf
        nrows = 2
        ylen = 8
        stitle = 'COVID-19 cases/deaths in {}'.format(state)
    
    if cumulative is True:
        stitle = 'Cumulative ' + stitle
        plotcol = 'case'
        fitcol = '_fitvals_case'
    else:
        stitle = stitle + ' per day'
        plotcol = '_diff'
        fitcol = '_fitvals_diff'

    fig, axs = plt.subplots(nrows=nrows)
    fig.set_size_inches(12, ylen)
    plt.suptitle(stitle)

    if nrows == 1:
        ax = axs
    else:
        ax = axs[0]
    ax.set_ylabel(ylabel1)
    ax.plot(df1.index, df1[plotcol], 'g.', label=ylabel1)
    if fit is True:
        ax.plot(df1.index, df1[fitcol], 'g')
    ax.grid()
    ax.legend()
    
    if nrows == 2:
        ax = axs[1]
        ax.set_ylabel(ylabel2)
        ax.plot(df2.index, df2[plotcol], 'b.', label=ylabel2)
        if fit is True:
            ax.plot(df2.index, df2[fitcol], 'b')
        ax.grid()
        ax.legend()
    
    if saveloc is not None:
        plt.savefig(saveloc, dpi=300, bbox_inches='tight')
    plt.show()
    return None

