import csv

print("=" * 60)
print("SAMPLE FAKE NEWS ARTICLES")
print("=" * 60)
with open('Fake.csv', 'r', encoding='utf-8') as f:
    r = csv.reader(f)
    h = next(r)
    for i, row in enumerate(r):
        if i >= 3:
            break
        print(f"\n--- FAKE #{i+1} (Title: {row[0][:80]}) ---")
        print(row[1][:500])

print("\n" + "=" * 60)
print("SAMPLE REAL NEWS ARTICLES")
print("=" * 60)
with open('True.csv', 'r', encoding='utf-8') as f:
    r = csv.reader(f)
    h = next(r)
    for i, row in enumerate(r):
        if i >= 3:
            break
        print(f"\n--- REAL #{i+1} (Title: {row[0][:80]}) ---")
        print(row[1][:500])
