def test__is_creator(chat, user_1, user_2):
    chat.creator = user_1

    assert not chat.creator == user_2