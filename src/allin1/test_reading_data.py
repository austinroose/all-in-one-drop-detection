import pandas as pd


def test_read_csv():
  segment_df = pd.read_csv(
    'data/harmonix/segments/0004_abc.txt',
    names=['start', 'name'],
    sep=r'\s+',
    engine='python',
  )
  beat_df = pd.read_csv(
    'data/harmonix/beats/0004_abc.txt',
    names=['time', 'count', 'bar'],
    sep=r'\s+',
    engine='python',
    usecols=[0, 1],
  )
  print(segment_df)
  print(beat_df.head())
  assert segment_df['start'].dtype.kind == 'f'
  assert beat_df['time'].dtype.kind == 'f'
  assert beat_df['count'].dtype.kind in 'iu'


if __name__ == '__main__':
  test_read_csv()
