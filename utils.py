from aiogram.utils.helper import Helper, HelperMode, ListItem


class TestStates(Helper):
    mode = HelperMode.snake_case

    MANGA_ADDITION_STATE = ListItem()
    MANGA_DELETE_STATE = ListItem()
    TEST_STATE_0 = ListItem()
    TEST_STATE_2 = ListItem()
    TEST_STATE_3 = ListItem()
    TEST_STATE_4 = ListItem()
    TEST_STATE_5 = ListItem()
