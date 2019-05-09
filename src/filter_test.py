"""
This script exists to test sets of filtering parameters derived from one file on
other files.
"""

from image_filter import ImageFilter

__author__ = 'Nick'

# apply given set of feature filters to all supplied files for manual assessment of 
# effectiveness of filters on given files
def test_filter_on_files(filters, paths):
    fil = ImageFilter(chosen_filters)
    for file in chosen_files:
        path = '../videos/' + file
        print 'testing {0}'.format(path)
        fil.test_filters(path, downsize_scale = 2)
