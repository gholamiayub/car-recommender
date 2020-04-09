import mysql.connector
from sklearn import tree


mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="admin",
  database='bama'
)
x, y = [], []

cursor = mydb.cursor()
query = 'SELECT * FROM ML;'
cursor.execute(query)

for (model, year, price, iD) in cursor:
    item = price, year
    x.append(list(item))
    y.append(model)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
car_price, car_year = tuple(map(int, input('Please enter price and year >>>\n').split()))
print('''>>>These models range from -5,000 to +5,000 >>> your chosen price\n''')
prices = -5000
num = 0
for item in range(0, 11000, 1000):
    range_price = car_price + prices + item # range prices from -5,000 to +5,000
    data = [[range_price, car_year]]
    answer = clf.predict(data)
    print(str(num)+': ', answer[0])
    num += 1

