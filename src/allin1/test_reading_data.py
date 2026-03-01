import pandas as pd

def test_read_csv():
    data = pd.read_csv(
        'data/harmonix/segments/0004_abc.txt',
        names=['start', 'name'],
        delimiter=r'\s+',  # Match any whitespace
        engine='python'    
    )
    print(data)

if __name__ == '__main__':
  test_read_csv()

