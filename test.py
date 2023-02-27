
from main import ADJ_FILE_PATH, COORD_FILE_PATH, get_adj, get_coord, get_best_first_path
import pytest

ADJ_TEST_FILE_PATH = 'adjacencies_test.txt'
COORD_TEST_FILE_PATH = 'coordinates_test.txt'

def test_get_adj() :

    exp_adj_dict = {
        'Anthony': ['Bluff_City', 'Kiowa', 'Attica', 'Harper'],
        'Attica': ['Medicine_Lodge'],
        'Augusta': ['Winfield', 'Andover', 'Leon', 'Wichita']
    }

    adj_dict = get_adj(ADJ_TEST_FILE_PATH)

    assert exp_adj_dict == adj_dict

def test_get_coord() :

    exp_coord_dict = {
        'Abilene': (38.9220277, -97.2666667),
        'Andover': (37.6868403, -97.1657752),
        'Anthony': (37.1575168, -98.0728946)
    }

    coord_dict = get_coord(COORD_TEST_FILE_PATH)

    assert exp_coord_dict == coord_dict

def test_get_best_first_path() :

    adj_dict = get_adj(ADJ_FILE_PATH)
    coord_dict = get_coord(COORD_FILE_PATH)

    # normal, but long path
    assert get_best_first_path(adj_dict, coord_dict, 'Topeka', 'Anthony') == \
        ['Topeka', 'Junction_City', 'Marion', 'Newton', 'Wichita', 'Cheney', 'Kingman', 'Pratt', 'Sawyer', 'Rago', 'Harper', 'Anthony']

    # same start and dest node
    assert get_best_first_path(adj_dict, coord_dict, 'Topeka', 'Topeka') == ['Topeka']

    # adjacent start and dest node
    assert get_best_first_path(adj_dict, coord_dict, 'Pratt', 'Kingman') == ['Pratt', 'Kingman']

