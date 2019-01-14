from datetime import date







class StockHandle:
    def __init__(self,stock_instance,odd_instance):
        self.stock_instance = stock_instance
        self.odd_instance = odd_instance




    # 入库处理
    def warehousing_handle(self,stock_instance, warehousing_data):
        old_unit_cost = stock_instance.unit_cost
        old_count = stock_instance.count
        unit_cost = warehousing_data.total_cost_price
        count = warehousing_data.count
        new_cost_price = (unit_cost * count + old_count * old_unit_cost) / (count + old_count)
        stock_instance.recent_date = date.today()
        stock_instance.unit_cost = new_cost_price
        stock_instance.save()

    # 出库处理
    def invoice_handle(self,stock_instance, invoice_data):
        old_unit_cost = stock_instance.unit_cost
        old_count = stock_instance.count
        unit_cost = invoice_data.total_cost_price
        count = invoice_data.count
        new_cost_price = (unit_cost * count + old_count * old_unit_cost) / (count + old_count)
        stock_instance.recent_date = date.today()
        stock_instance.save()

    # 出入库记录
    def add_record(self,stock_instance, num, type):


        pass
