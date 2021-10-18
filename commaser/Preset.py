class BasePreset(object):
    take_profit = 1.5
    take_profit_type = 'total'
    active_safety_orders_count = 1

    strategy_list = [{"strategy": "nonstop"}]
    start_order_type = 'limit'


class Size(object):
    base_order_volume = 10
    safety_order_volume = 20


class TAS1(BasePreset, Size):

    max_safety_orders = 25
    safety_order_step_percentage = 2.4

    martingale_volume_coefficient = 1.05
    martingale_step_coefficient = 1


class HF1(BasePreset, Size):

    max_safety_orders = 25
    safety_order_step_percentage = 0.24

    martingale_volume_coefficient = 1.05
    martingale_step_coefficient = 1
