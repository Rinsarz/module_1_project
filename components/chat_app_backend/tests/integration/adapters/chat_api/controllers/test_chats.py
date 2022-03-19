import datetime


def test__on_get_show_messages(client, chats_service,
                               message_from_user_1_chat_1,
                               date_string_1):

    message_from_user_1_chat_1.user_id = 1
    message_from_user_1_chat_1.chat_id = 3
    message_from_user_1_chat_1.message_id = 1
    message_from_user_1_chat_1.message_text = 'test message text'
    message_from_user_1_chat_1.created = datetime.datetime.strptime(date_string_1, "%d-%m-%Y %H:%M:%S")

    messages = [
        message_from_user_1_chat_1
        ]

    chats_service.get_messages.return_value = messages

    expected = {
        'messages': [
            {
                'message_id': 1,
                'message_text': 'test message text',
                'message_author_id': 1,
                'message_created': date_string_1
                },
            ]
        }

    result = client.simulate_get('/api/chats/show_messages', )
    assert result.status_code == 200
    assert result.json == expected