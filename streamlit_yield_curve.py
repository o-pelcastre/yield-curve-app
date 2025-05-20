# Automatically install required packages if missing
import subprocess, sys
for pkg in ['streamlit', 'pandas', 'numpy', 'pandas_datareader', 'plotly']:
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])

import streamlit as st
import pandas as pd
import numpy as np
import pandas_datareader as pdr
import datetime as dt
import plotly.express as px

st.set_page_config(page_title='Yield Curve App', layout='wide')
st.title('Yield Curve Visualization')

# Fetch data
start = dt.datetime(2018, 3, 1)
end = dt.date.today()
yield_curve_maturities = ['DGS1MO', 'DGS3MO', 'DGS6MO', 'DGS1', 'DGS2', 'DGS5', 'DGS7', 'DGS10', 'DGS20', 'DGS30']
yield_data = []
for mat in yield_curve_maturities:
    yield_data.append(pdr.DataReader(mat, 'fred', start, end))
yield_curve = pd.concat(yield_data, axis=1)
yield_curve.columns = yield_curve_maturities
yield_curve = yield_curve.dropna()

# Sidebar date selector
date_selected = st.sidebar.slider(
    'Select Date',
    min_value=yield_curve.index.min().date(),
    max_value=yield_curve.index.max().date(),
    value=yield_curve.index.max().date()
)

# Plot yield curve for chosen date
yc_on_date = yield_curve.loc[str(date_selected)]
fig1 = px.line(
    x=yc_on_date.index,
    y=yc_on_date.values,
    labels={'x': 'Maturity', 'y': 'Yield'},
    title=f'Yield Curve on {date_selected}'
)
st.plotly_chart(fig1, use_container_width=True)

# Animated yield curve over time
df_anim = yield_curve.reset_index().melt(
    id_vars='index', var_name='Maturity', value_name='Yield'
)
df_anim.rename(columns={'index':'Date'}, inplace=True)
fig_anim = px.line(
    df_anim, x='Maturity', y='Yield',
    animation_frame='Date',
    range_y=[0, yield_curve.values.max()*1.1],
    labels={'Yield':'Yield', 'Maturity':'Maturity'},
    title='Yield Curve Animation (2018 - Today)'
)
st.plotly_chart(fig_anim, use_container_width=True)