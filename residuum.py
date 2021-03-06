import pandas as pd
import matplotlib.pyplot as plt

# Ux_final, Uz_final, p_final
want_see = 'Ux_final'

fpath = '../NacaAirfoil/postProcessing/solverInfo/0/solverInfo.dat'

df = pd.read_csv(fpath, sep='\t', skiprows=1)
df.columns = [x.strip() for x in df.columns]
df.rename(columns={'# Time': 'time'}, inplace=True)
# print(df.head())

plt.rcParams['figure.figsize'] = (8,6)
plt.semilogy(df['time'], df[want_see])
plt.xlabel('time')
plt.ylabel(want_see)
plt.grid(True, alpha=0.5)
plt.show()