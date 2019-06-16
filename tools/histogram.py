# pylint:skip-file
"Код для экспериментов с распределениями"
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from constants import DATE_FORMAT
start_moscow = datetime.strptime('01.09.1941', DATE_FORMAT)
end_moscow = datetime.strptime('31.01.1942', DATE_FORMAT)
start_stalin = datetime.strptime('01.07.1942', DATE_FORMAT)
end_stalin = datetime.strptime('28.02.1943', DATE_FORMAT)
moscow_length = end_moscow - start_moscow
stalin_length = end_stalin - start_stalin
size=moscow_length.days + stalin_length.days
wtype_diversity = 50
# z = np.random.weibull(3.)
d = dict()
a = 10 # 2.05 #15
for i in range(size):
    d[i] = round(np.random.weibull(a) * wtype_diversity / a)
# z = np.random.weibull(3., size=size)
# z *= scale
plt.hist(d.values(), bins=range(wtype_diversity), density=True)
plt.title("Гистограмма типов погоды")
plt.xlabel("Номера типов погоды")
plt.ylabel("Доля типа погоды среди всех")
plt.show()
