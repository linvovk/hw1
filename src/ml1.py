import random
from datetime import datetime, timedelta
from sklearn.tree import DecisionTreeClassifier

def generate_transactions(num=20):
    transactions = []
    users = ['User1', 'User2', 'User3', 'User4', 'User5']
    countries = ['USA', 'UK', 'DE', 'RU', 'CN', 'FR', 'JP']
    start_time = datetime.now() - timedelta(days=1)
    
    for i in range(num):
        t = {'id': f'TXN{i+1}',
            'user': random.choice(users),
            'amount': round(random.uniform(100, 20000), 2),
            'time': start_time + timedelta(hours=random.randint(0, 23)),
            'country': random.choice(countries)}
        transactions.append(t)
    
    return sorted(transactions, key=lambda x: x['time'])

def fraud_detection(transactions, limit=10000, freq=5, bad=['RU', 'CN']):
    X = []
    y = []
    for i in range(50):
        X.append([random.uniform(100,20000), random.randint(0,1)])
        y.append(1 if X[-1][0] > 8000 and X[-1][1] == 1 else 0)
    model = DecisionTreeClassifier()
    model.fit(X, y)
    
    report = []
    history = {}
    
    for t in transactions:
        user = t['user']
        amount = t['amount']
        country = t['country']

        if user not in history:
            history[user] = []
        history[user].append(t['time'])
        recent = [x for x in history[user] if x > t['time'] - timedelta(hours=1)]
        high_freq = len(recent) > freq

        cur_limit = limit / 2 if country in bad else limit
        high_amount = amount > cur_limit
  
        risk = 1 if country in bad else 0
        ml = model.predict([[amount, risk]])[0]
        
        # Вердикт
        if high_amount and country in bad:
            status = 'BLOCKED'
        elif ml == 1:
            status = 'FLAGGED_ML'
        elif high_amount:
            status = 'FLAGGED_AMOUNT'
        elif high_freq:
            status = 'FLAGGED_FREQ'
        else:
            status = 'APPROVED'
        
        report.append([t['id'], user, amount, country, status])
    
    return report

t = generate_transactions(15)
r = fraud_detection(t)

for line in r:
    print(f"{line[0]} {line[1]} {line[2]:8.2f} {line[3]} {line[4]}")
