# -*- coding: utf-8 -*-
import time
import datetime

from analysis.utils import connect_postgresql, disconnect_postgresql


def get_factory_id(phone):
    cur = connect_postgresql()
    cur.execute("select factory from factory_users where phone = '%s';" % phone)
    tmp = cur.fetchall()
    factory_id = tmp[0][0] if tmp else None
    # 如果号码不存在？
    return factory_id


def get_week_timestamp():
    # return the timestamp of monday
    num_in_week = datetime.datetime.now().weekday()
    dtime = datetime.datetime.now().strftime('%Y-%m-%d')
    today = datetime.datetime.strptime(dtime, '%Y-%m-%d')
    monday = today + datetime.timedelta(days=-num_in_week)
    timestamp = int(time.mktime(monday.timetuple()))
    return timestamp


def get_month_timestamp(num):
    # return two timestamps about month, start_timestamp and end_timestamp
    # 0: this month
    # 1: last month
    # ...
    now = datetime.datetime.now()
    correct_time_1 = correct_time(now.year, now.month - num)
    start = datetime.datetime(correct_time_1[0], correct_time_1[1], 1)
    correct_time_2 = correct_time(now.year, now.month - (num - 1))
    end = datetime.datetime(correct_time_2[0], correct_time_2[1], 1) - datetime.timedelta(seconds=1)
    start_timestamp = int(time.mktime(start.timetuple()))
    end_timestamp = int(time.mktime(end.timetuple()))
    return start_timestamp, end_timestamp


def get_salesman(cur, timestamp, factory_id):
    cur.execute(
        "select creator, sum(b.product_count * b.sell_price) as price from orders as a, order_products as b where a.factory = '%s' and a.deliver_time > %d and a.id = b.order_id and b.product_count is not null group by creator order by price desc;" % (
            factory_id, timestamp))
    tmp = cur.fetchall()
    phone, sales = tmp[0] if tmp else (None, 0)
    if sales is None:
        sales = 0
    cur.execute("select name, image from user_info where phone = '%s';" % phone)
    tmp = cur.fetchall()
    if tmp:
        if isinstance(tmp[0][0], (list, tuple)):
            name = ''.join(tmp[0][0])
        elif isinstance(tmp[0][0], memoryview):
            name = tmp[0][0].tobytes()
        else:
            name = tmp[0][0] or ''
        if isinstance(tmp[0][1], (list, tuple)):
            image = ''.join(tmp[0][1])
        elif isinstance(tmp[0][1], memoryview):
            image = tmp[0][1].tobytes()
        else:
            image = tmp[0][1]
    else:
        name = ''
        image = ''

    return name, image, sales


def get_sales(cur, start_timestamp, end_timestamp, factory_id):
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_timestamp)))
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_timestamp)))
    cur.execute(
        "select sum(product_count * sell_price) as price from order_products where order_id in (select id from orders where factory = '%s' and time between %d and %d);" % (
            factory_id,
            start_timestamp, end_timestamp))
    tmp = cur.fetchall()
    sales = tmp[0][0] if tmp and tmp[0] else 0
    if not sales:
        sales = 0
    return sales


def correct_time(year, month):
    if month <= 0:
        return year - 1, month + 12
    elif month > 12:
        return year + 1, month - 12
    else:
        return year, month


def finance_format(finance):
    # recieve a float or int
    if isinstance(finance, int):
        return format(finance, ',') + '.00'
    elif isinstance(finance, float):
        finance = round(finance, 2)
        tmp = str(finance)
        if tmp[-2] == '.':
            return format(finance, ',') + '0'
        else:
            return format(finance, ',')


def purchase(cur, start_timestamp, end_timestamp, factory_id):
    cur.execute(
        "select material_type_id, sum(total_price) as price from purchase where factory = '%s' and buy_time between %d and %d group by material_type_id order by price desc;" % (
            factory_id, start_timestamp, end_timestamp))
    tmp = cur.fetchall()
    length = len(tmp)

    result = []
    top_three = tmp[:3]
    other = sum(i[1] for i in tmp[3:])

    for i in top_three:
        cur.execute(
            "select a.name, b.name from material_types as a, material_categories as b where a.id = '%s' and b.id = a.category_id;" %
            i[0])
        data = cur.fetchall()
        if data:
            tmp = {}
            tmp['name'] = data[0][0]
            tmp['category_name'] = data[0][1]
            tmp['cost'] = finance_format(i[1])
            result.append(tmp)
        else:
            tmp = {}
            tmp['name'] = None
            tmp['category_name'] = None
            tmp['cost'] = finance_format(i[1])
            result.append(tmp)
    if length > 3:
        tmp = {}
        tmp['category_name'] = '其他'
        tmp['cost'] = finance_format(other)
        result.append(tmp)
    return result


def month_part():
    # month
    month = int(datetime.datetime.now().strftime('%m'))
    return month


def order_part(factory_id):
    # order
    cur = connect_postgresql()

    start_timestamp = get_week_timestamp()
    end_timestamp = time.mktime(datetime.datetime.now().timetuple())
    w_sales = get_sales(cur, start_timestamp, end_timestamp, factory_id)

    w_champ_name, w_champ_id, w_champ_sales = get_salesman(cur, start_timestamp, factory_id)

    start_timestamp, end_timestamp = get_month_timestamp(0)
    m_sales = get_sales(cur, start_timestamp, end_timestamp, factory_id)
    m_champ_name, m_champ_id, m_champ_sales = get_salesman(cur, start_timestamp, factory_id)

    start_timestamp, end_timestamp = get_month_timestamp(1)
    lm_sales = get_sales(cur, start_timestamp, end_timestamp, factory_id)

    m_rose = round((m_sales - lm_sales) / lm_sales * 100, 2) if lm_sales else 0

    order = {}
    order['w_sales'] = finance_format(w_sales)
    order['w_champ_sales'] = finance_format(w_champ_sales)
    order['w_champ_id'] = w_champ_id
    order['w_champ_name'] = w_champ_name
    order['m_sales'] = finance_format(m_sales)
    order['m_rose'] = m_rose
    order['m_champ_sales'] = finance_format(m_champ_sales)
    order['m_champ_id'] = m_champ_id
    order['m_champ_name'] = m_champ_name

    disconnect_postgresql(cur)
    return order


def finance_part(factory_id):
    # finance
    cur = connect_postgresql()

    start_timestamp, end_timestamp = get_month_timestamp(0)
    month_0 = get_sales(cur, start_timestamp, end_timestamp, factory_id)
    start_timestamp, end_timestamp = get_month_timestamp(1)
    month_1 = get_sales(cur, start_timestamp, end_timestamp, factory_id)

    rose = month_0 - month_1
    four_months = []

    start_timestamp, end_timestamp = get_month_timestamp(2)
    month_2 = get_sales(cur, start_timestamp, end_timestamp, factory_id)
    start_timestamp, end_timestamp = get_month_timestamp(3)
    month_3 = get_sales(cur, start_timestamp, end_timestamp, factory_id)

    month = month_part()
    four_months.append({'m': str(month), 'sales': finance_format(month_0)})
    four_months.append({'m': str(correct_time(0, month - 1)[1]), 'sales': finance_format(month_1)})
    four_months.append({'m': str(correct_time(0, month - 2)[1]), 'sales': finance_format(month_2)})
    four_months.append({'m': str(correct_time(0, month - 3)[1]), 'sales': finance_format(month_3)})

    finance = {}
    finance['rose'] = finance_format(rose)
    finance['list'] = four_months

    disconnect_postgresql(cur)
    return finance


def purchase_part(factory_id):
    # purchase
    cur = connect_postgresql()

    start_timestamp = get_week_timestamp()
    end_timestamp = time.mktime(datetime.datetime.now().timetuple())
    w = purchase(cur, start_timestamp, end_timestamp, factory_id)
    start_timestamp, end_timestamp = get_month_timestamp(1)
    m = purchase(cur, start_timestamp, end_timestamp, factory_id)
    material = {'w': w, 'm': m}

    disconnect_postgresql(cur)
    return material


def run(factory_id):
    # result
    result = {}
    result['month'] = str(month_part())
    result['order'] = order_part(factory_id)
    result['finance'] = finance_part(factory_id)
    result['material'] = purchase_part(factory_id)
    return result


if __name__ == '__main__':
    test = run('')
    print(test)
