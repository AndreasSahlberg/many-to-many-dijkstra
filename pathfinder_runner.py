from pathfinder import *
import pandas as pd

test_data = pd.read_csv('test_data.csv')

origins = test_data.pivot('Y', 'X', 'ElecStart')
origins.fillna(value=0, inplace=True)
axis_labels = origins
origins = origins.to_numpy()

targets = test_data[['Y', 'X', 'MinimumOverallCode']]
targets['MinimumOverallCode'] = targets.where(targets['MinimumOverallCode']==1, other=0)
targets = targets.pivot('Y', 'X', 'MinimumOverallCode')
targets.fillna(value=0, inplace=True)
targets = targets.to_numpy()
# Remove ElecStart from targets ???

weights = test_data[['Y', 'X', 'RoadDist']]
weights = weights.pivot('Y', 'X', 'RoadDist')
weights.interpolate(limit=10, inplace=True)
weights.fillna(value=999, inplace=True)
weights = weights.to_numpy()

pathfinder = seek(origins, targets, weights, path_handling='link', debug=False, film=True)

paths = pd.DataFrame(pathfinder['paths'])
paths.set_axis(axis_labels.axes[1], axis='columns', inplace=True)
paths.set_axis(axis_labels.axes[0], axis='rows', inplace=True)
paths = paths.unstack()
paths = paths.loc[lambda paths: paths > 0]
paths.to_csv('paths.csv')

distances = pd.DataFrame(pathfinder['distance'])
distances.set_axis(axis_labels.axes[1], axis='columns', inplace=True)
distances.set_axis(axis_labels.axes[0], axis='rows', inplace=True)
distances = distances.unstack()
distances = distances.loc[lambda distances: distances == 0]
distances.to_csv('distances.csv')


