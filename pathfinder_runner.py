from pathfinder import *
import pandas as pd

test_data = pd.read_csv('test_data.csv')

origins = test_data.pivot('Y', 'X', 'ElecStart')
origins.fillna(value=0, inplace=True)
origins = origins.to_numpy()

targets = test_data[['Y', 'X', 'MinimumOverallCode']]
targets['MinimumOverallCode'] = targets.where(targets['MinimumOverallCode']==1, other=0)
targets = targets.pivot('Y', 'X', 'MinimumOverallCode')
targets.fillna(value=0, inplace=True)
targets = targets.to_numpy()
# Remove ElecStart from targets ???

weights = test_data[['Y', 'X', 'GridPenalty']]
weights = weights.pivot('Y', 'X', 'GridPenalty')
weights.fillna(value=1, inplace=True)
weights = weights.to_numpy()

pathfinder = seek(origins, targets, weights, path_handling='link', debug=False, film=True)

paths = pd.DataFrame(paths)
paths.to_csv('paths.csv')
