class BasePreset(object):
    take_profit = 1.5
    take_profit_type = 'total'
    active_safety_orders_count = 1

    strategy_list = [{"strategy": "nonstop"}]
    start_order_type = 'limit'


class Size1(object):
    base_order_volume = 10
    safety_order_volume = 20


class Size2(object):
    base_order_volume = 20
    safety_order_volume = 40


class TAS1(BasePreset, Size1):
    max_safety_orders = 25
    safety_order_step_percentage = 2.4

    martingale_volume_coefficient = 1.05
    martingale_step_coefficient = 1


class HFS1(BasePreset, Size1):
    max_safety_orders = 25
    safety_order_step_percentage = 0.24

    martingale_volume_coefficient = 1.05
    martingale_step_coefficient = 1


class TAS2(BasePreset, Size2):
    max_safety_orders = 25
    safety_order_step_percentage = 2.4

    martingale_volume_coefficient = 1.05
    martingale_step_coefficient = 1


presets = {
    TAS1.__name__: TAS1,
    TAS2.__name__: TAS2,
    HFS1.__name__: HFS1,

}
