class Bot(object):
    def __init__(self):
        self.id
        self.account_id
        self.is_enabled

        self.deletable
        self.trailing_enabled
        self.name

        self.preset = Preset()

        self.tags = []


class Preset(object):
    def __init__(self):
        self.base_order
        self.safety_order

        self.take_profit

        self.max_safety_orders
        self.active_safety_orders_count

        self.safety_order_step_percentage
        self.safety_order_volume_scale
        self.safety_order_step_scale
