from pyfcm import FCMNotification

push_service = FCMNotification(api_key='')


def notify_single_device(message_title, message_body, registration_id):
    result = push_service.notify_single_device(message_title=message_title,
                                               message_body=message_body,
                                               registration_id=registration_id)

    return result


def notify_multiple_devices(message_title, message_body, registration_ids):
    result = push_service.notify_multiple_devices(message_title=message_title,
                                                  message_body=message_body,
                                                  registration_ids=registration_ids)

    return result


def notify_topic_subscribers(message_title, message_body, topic_name):
    result = push_service.notify_topic_subscribers(message_title=message_title,
                                                   message_body=message_body,
                                                   topic_name=topic_name)

    return result
