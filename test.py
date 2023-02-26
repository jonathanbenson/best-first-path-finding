
from main import get_adj
import pytest

ADJACENCIES_FILE_PATH = 'adjacencies_test.txt'

def test_get_adj() :

    exp_adj_dict = {
        'Anthony': ['Bluff_City', 'Kiowa', 'Attica', 'Harper'],
        'Attica': ['Medicine_Lodge'],
        'Augusta': ['Winfield', 'Andover', 'Leon', 'Wichita']
    }

    adj_dict = get_adj(ADJACENCIES_FILE_PATH)

    assert exp_adj_dict == adj_dict
