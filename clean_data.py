# importing libraries
from datetime import datetime
import os
import sys
import time

import pandas as pd
import numpy as np


def ensure_dir(dir_path):
    """
    Check if directory exists, else create it.

    Keyword arguments:
    dir_path -- directory path
    """
    directory = os.path.dirname(dir_path)
    if not os.path.exists(directory):
        print('Directory Exception: ' + dir_path +
              ' not available, creating now...')
        os.makedirs(directory)


def change_timestamp(source_file_path, dest_file_path, ts_colnames):
    """
    Read file, change column name to timestamp and save it to new destination

    Keyword arguments:
    source_file_path -- file to read from
    dest_file_path -- file to read into
    ts_columns -- list of column names to update
    """
    # reading file as a dataframe
    file = pd.read_csv(source_file_path, sep='\t')

    # changing respective column name to Timestamp
    cols = np.array(file.columns)
    cols[file.columns.isin(ts_colnames)] = 'Timestamp'
    file.columns = cols

    # moving timestamp to first column
    cols = list(cols)
    cols.insert(0, cols.pop(cols.index('Timestamp')))
    file = file[cols]

    # ensure directory exists
    ensure_dir(os.path.join(os.path.split(dest_file_path)[0], ""))

    # reading first timestamp and saving as new dir structure
    ts = datetime.strptime(file['Timestamp'].iloc[0], '%Y-%m-%d %H:%M:%S')
    dest_file_path_split = dest_file_path.split(os.sep)
    dest_file_path_split[2] = ts.strftime("%Y")
    dest_file_path_split[3] = ts.strftime("%Y-%m")
    dest_file_path = os.path.join(*dest_file_path_split)

    # saving file in new directory
    file.to_csv(dest_file_path, index=False, sep='\t', na_rep='NULL')


def traversal_modify(source='data', destination='submission', ts_colnames=['i32', 'm63', 'w23']):
    """
    Traverse the source folder, modify the column names then store resulting file in destination folder

    Keyword arguments:
    source -- directory to copy from
    destination -- directory to copy to
    ts_colnames -- list of column names to update
    """
    for root, dirs, files in os.walk(source):

        # skipping all hidden files
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        # dirs return empty when on leaf of folder structure
        if not dirs:
            root_dest = root.replace(source, destination)

            for f in files:
                # modifying file
                change_timestamp(source_file_path=os.path.join(root, f),
                                 dest_file_path=os.path.join(root_dest, f),
                                 ts_colnames=ts_colnames)


if __name__ == "main":
    start = time.time()
    traversal_modify(
        source=sys.argv[0], destination=sys.argv[1], ts_colnames=sys.argv[2:])
    end = time.time()
    print("Successfully executed in {:.2f}s".format(end - start))
else:
    start = time.time()
    traversal_modify()
    end = time.time()
    print("Successfully executed in {:.2f}s".format(end - start))
