class BasePreset(object):
    take_profit = 1.5
    take_profit_type = 'total'
    active_safety_orders_count = 1

    strategy_list = [{"strategy": "nonstop"}]
    start_order_type = 'limit'


class Size1(object):
    base_order_volume = 10
    safety_order_volume = 20


class TA_S1(BasePreset, Size1):
    max_safety_orders = 25
    safety_order_step_percentage = 2.4

    martingale_volume_coefficient = 1.05
    martingale_step_coefficient = 1


class HF_S1(BasePreset, Size1):
    max_safety_orders = 25
    safety_order_step_percentage = 0.24

    martingale_volume_coefficient = 1.05
    martingale_step_coefficient = 1


presets = {
    TA_S1.__name__: TA_S1,
    HF_S1.__name__: HF_S1
}
