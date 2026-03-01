import random
from datetime import datetime, timedelta

def generate_transactions(num=20):
    transactions = []
    users = ['User1', 'User2', 'User3', 'User4', 'User5']
    countries = ['USA', 'UK', 'DE', 'RU', 'CN', 'FR', 'JP']

    start_time = datetime.now() - timedelta(days=1)

    for i in range(num):
        transaction = {'id': f'TXN{i+1:03d}',
            'user': random.choice(users),
            'amount': round(random.uniform(100, 20000), 2),
            'time': start_time + timedelta(hours=random.randint(0, 23),
                                          minutes=random.randint(0, 59)),
            'country': random.choice(countries)}
        transactions.append(transaction)

    return sorted(transactions, key=lambda x: x['time'])

def fraud_detection(transactions, amount_limit=10000, freq_limit=5,
                    high_risk_countries=['RU', 'CN']):
    """Проверяет транзакции на фрод"""
    report = []
    user_history = {}

    for t in transactions:
        user = t['user']
        amount = t['amount']
        country = t['country']
        time = t['time']

        if user not in user_history:
            user_history[user] = []

        hour_ago = time - timedelta(hours=1)
        recent = [x for x in user_history[user] if x > hour_ago]
        user_history[user] = recent + [time]
        high_freq = len(recent) >= freq_limit

        current_limit = amount_limit / 2 if country in high_risk_countries else amount_limit
        high_amount = amount > current_limit

        if high_amount and country in high_risk_countries:
            status = 'BLOCKED: High Risk Country & Amount'
        elif high_amount:
            status = 'FLAGGED: High Amount'
        elif high_freq:
            status = 'FLAGGED: High Frequency'
        else:
            status = 'APPROVED'

        report.append({'id': t['id'],
            'user': user,
            'amount': amount,
            'country': country,
            'time': time.strftime('%H:%M'),
            'status': status})

    return report

if __name__ == '__main__':
    transactions = generate_transactions(15)

    report = fraud_detection(transactions)
    for r in report:
        print(f"{r['id']} | {r['user']} | {r['amount']:8.2f} | "
              f"{r['country']} | {r['time']} | {r['status']}")

    stats = {}
    for r in report:
        stats[r['status']] = stats.get(r['status'], 0) + 1

    for status, count in stats.items():
        print(f'{status}: {count}')
