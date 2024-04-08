import paneltime as pt
import pandas as pd
import numpy as np
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import adfuller


pt.options.fixed_random_group_eff.set(0)
pt.options.fixed_random_time_eff.set(0)
pt.options.EGARCH.set(False)
pt.options.tolerance.set(0.01)
pt.options.supress_output.set(True)


def main():
	if False:
		real_news = pd.read_excel("RealNewsDjiaReturns.xlsx")
		real_news = real_news.rename(columns={'Real News':'News_sentiment'})
		real_news = real_news.fillna(0)
		
		e = estimate2(real_news[['News_sentiment']])
		real_news = real_news [4:]
		real_news ['News_Change'] = e

		
		
		real_news['LNews_Change1'] = real_news['News_Change'].shift(1)

		real_news = real_news.dropna()
		pt.options.pqdkm.set([1,1,0,2,2])
		s = pt.execute("return~News_Change+LNews_Change1",real_news,T='Date')

		print(s)

	if True:
		real_news = pd.read_excel("RealNewsDjiaReturns.xlsx")
		real_news = real_news.rename(columns={'Real News':'News_sentiment'})
		real_news = real_news.fillna(0)
		estimate(real_news, 'News_sentiment')
	a=0



def estimate2(df):


	# Check for stationarity. If p > 0.05, difference the series.
	result = adfuller(df)
	if result[1] > 0.05:
		df = df.diff().dropna()

	errors = []

	for t in range(4, len(df)):
		train = df.iloc[:t]
		test = df.iloc[t]
		
		model = AutoReg(train, lags=1)
		model_fit = model.fit()
		
		prediction = model_fit.predict(start=len(train), end=len(train))
		
		# Check if the prediction is nan.
		if not np.isnan(prediction.iloc[0]):
			error = test - prediction.iloc[0]
			errors.append(error)

	# Convert errors to a numpy array
	return np.array(errors)

def estimate(df,name):
	df_name = df[[name]]
	errors = []
	start =4
	for t in range(start, len(df)):
		train = df_name.iloc[:t]
		test = df_name.iloc[t]
		
		if True:
			model = AutoReg(train, lags=1)
			model_fit = model.fit()
			p = model_fit.predict(start=len(train), end=len(train))
			prediction = float(p)
		else:
			pt.options.pqdkm.set([1,0,0,0,0])
			s = pt.execute("News_sentiment",train,T='Date')
			prediction = s.predict()['predicted residual']
		
		error = test - prediction
		
		#print(f"{t}:{prediction}; errors:{abs(float(error))} ")
		errors.append(error)

	# Convert errors to a numpy array
	errors = np.array(errors)

	df = df [start:]
	df['News_Change'] = errors
	df['LNews_Change1'] = df['News_Change'].shift(1)

	df = df.dropna()

	pt.options.pqdkm.set([1,1,0,2,2])
	s = pt.execute("return~News_Change+LNews_Change1",df,T='Date')

	print(s)
	a=0



main()