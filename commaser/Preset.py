class BasePreset(object):
    def __init__(self):
        self.base_order
        self.safety_order

        self.take_profit

        self.max_safety_orders
        self.active_safety_orders_count

        self.safety_order_step_percentage
        self.safety_order_volume_scale
        self.safety_order_step_scale


class TAS1(BasePreset):
    def __init__(self):
        self.pairs = []
        self.bots = []
        self.exchanges = []
