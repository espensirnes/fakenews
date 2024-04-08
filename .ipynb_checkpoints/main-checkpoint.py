import paneltime as pt
import pandas as pd


pt.options.pqdkm.set([1,1,0,2,2])
pt.options.fixed_random_group_eff.set(0)
pt.options.fixed_random_time_eff.set(0)
pt.options.EGARCH.set(False)





print("FAKE NEWS****************************")
df = pd.read_excel("FakeNewsDjiaReturn.xlsx")
df = df.rename(columns={'News sentiment':'News_sentiment'})


df['LNews_sentiment1'] = df['News_sentiment'].shift(1)
df = df.dropna()

s = pt.execute("return~LNews_sentiment1",df,T='Date')

print(s)

print("****************************\n\n\n\n\n")

print("REAL NEWS ************************************")
df = pd.read_excel("RealNewsDjiaReturns.xlsx")
df = df.rename(columns={'Real News':'Real_news'})


df['LRealNews1'] = df['Real_news'].shift(1)
df = df.dropna()

s = pt.execute("return~LRealNews1",df,T='Date')
print(s)











