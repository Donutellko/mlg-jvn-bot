SUBSCRIPTION_KEY = "SUBSCRIPTION_KEY"
LAST_SAVED_PLAZAS_KEY = 'LAST_SAVED_PLAZAS_KEY'


def get_or_save_key(user_data: dict, key: str, to_save: object = None):
    if to_save is None:
        return user_data.get(key)
    user_data[key] = to_save
    return to_save


def subscriptions(user_data: dict, to_save: list = None) -> list:
    """
    is a list of dicts:
    { LAST_SAVED_CITAS_KEY }
    """
    return get_or_save_key(user_data, SUBSCRIPTION_KEY, to_save)


def add_subscription(user_data: dict, actual_plazas: []):
    subs = subscriptions(user_data) or []

    subscription = {
        LAST_SAVED_PLAZAS_KEY: actual_plazas
    }
    subs.append(subscription)
    subscriptions(user_data, subs)


def reset_subscriptions(user_data: dict):
    get_or_save_key(user_data, SUBSCRIPTION_KEY, [])


def is_subscribed_citas(user_data: dict) -> bool:
    subscriptions: list = get_or_save_key(user_data, SUBSCRIPTION_KEY)
    return subscriptions is not None and len(subscriptions) > 0

