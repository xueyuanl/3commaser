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


class Strategy(object):
    def __init__(self, code, **kwargs):
        self.code = code
        self.take_profit = kwargs.get('TP', 1.5)
        self.base_order_volume = kwargs['BO']
        self.safety_order_volume = kwargs['SO']
        self.max_safety_orders = kwargs['MSTC']
        self.safety_order_step_percentage = kwargs['SOS']
        self.martingale_volume_coefficient = kwargs['OS']
        self.martingale_step_coefficient = kwargs['SS']
        # some default values
        self.take_profit_type = 'total'
        self.active_safety_orders_count = 1
        self.strategy_list = kwargs.get('strategy_list', [{"strategy": "nonstop"}])
        self.start_order_type = 'limit'

        self.disable_after_deals_count = kwargs.get('disable_after_deals_count', None)


presets = {
    TAS1.__name__: TAS1,
    TAS2.__name__: TAS2,
    HFS1.__name__: HFS1,

}
