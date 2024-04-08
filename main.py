import paneltime as pt
import pandas as pd
import os
import numpy as np


pt.options.pqdkm.set([1,1,0,1,1])
pt.options.fixed_random_group_eff.set(0)
pt.options.fixed_random_time_eff.set(0)
pt.options.EGARCH.set(False)
pt.options.tolerance.set(0.00001)


def main():
	analyze_all()
	organize()


def analyze_all():
	done = []
	c = ('lags', 'true', 'regname', 'coef name', 'coef', 'std err', '  ', 
	  '[0.025  ','  0.975]', 't', 'P>|t|', 'CI', 'CI vars', 'r2 adj', 'r2')
	res = pd.DataFrame(columns=c)
	for f in os.listdir('data'):
		f_ = f.replace('True','').replace('Fake', '')
		if not f_ in done:
			done.append(f_)
			res = analyze(done[-1], res, True,  c)
			res = analyze(done[-1], res, False, c)
	res.to_pickle('results.pd')

def organize():
	res = pd.read_pickle('results.pd')
	df = res[(res['coef name'].isin(['L(News_sentiment,1)', 'L(News_sentiment,0)', 'L(News_sentiment,-1)']))]
	print('CI problems:')
	print(df.pivot(index='regname', columns=['true', 'coef name'], values= 'CI'))
	print(df.pivot(index='regname', columns=['true', 'coef name'], values= 'CI vars'))
	print(df.pivot(index='regname', columns=['true', 'coef name'], values= 'r2 adj'))
	print(df.pivot(index='regname', columns=['true', 'coef name'], values= 'r2'))

	coef = np.round(100*df['coef'],1).astype(str)
	stderr = np.round(100*df['std err'],2).astype(str)
	sign = df['  '].str.ljust(3)
	df['out'] = coef + '(' + stderr + ')' + sign
	df = df.pivot(index='regname', columns=['true', 'coef name'], values= 'out')
	print(df)
	df.to_excel('results.xlsx')
	a=0

def analyze(name, res, true, columns):
	df = pd.read_excel(f"data/{['Fake','True'][true]}{name}")
	df = df.rename(columns={'News sentiment':'News_sentiment', 
						 	'return':'ret'
							})

	name = name.replace('Returns.xlsx', '').replace('News', '')
	print(f"Estimating {str(true)} news for {name}")

	#out_ret = get_outliers(df, 'ret')
	#out_news = get_outliers(df, 'News_sentiment')
	#df = df[(out_ret+out_news)==0]
	
	for v in [1, 0, -1]:
		s = pt.execute(f"ret~L(News_sentiment,{v})",df,T='Date')
		n = len(s.coef_names)
		output = [[v]*n, [str(true)]*n, [name]*n, s.coef_names, s.coef_params, s.coef_se_robust,
				s.coef_codes , s.coef_025 , s.coef_0975,
				s.coef_tstat, s.coef_tsign, [s.CI]*n,[s.CI_n]*n,[s.statistics.Rsqadj_st]*n,[s.statistics.Rsq]*n ]
		r = pd.DataFrame(list(zip(*output)), columns = columns)
		res = pd.concat((res, r))

	return res


def get_outliers(df, name):
	n = len(df)
	k = int(len(df)*0.005)
	s = np.array(df[name])
	srt = np.sort(s)
	outliers = (s <srt[k]) + (s>srt[-k])

	return outliers


main()







