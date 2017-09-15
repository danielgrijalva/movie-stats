import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('data.csv')

plt.plot(data['year'], data['gross'])
plt.show()
