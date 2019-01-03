# -*- coding: utf-8 -*-
import datetime
import time

from analysis.retrieve_jcj import get_month_timestamp
from analysis.utils import disconnect_postgresql, connect_postgresql


def week_timestamp():
    """从本周当前某天到本周第一天的持续时间，时间戳"""
    num_in_week = datetime.datetime.now().weekday()
    dtime = datetime.datetime.now().strftime('%Y-%m-%d')
    today = datetime.datetime.strptime(dtime, '%Y-%m-%d')
    monday = today + datetime.timedelta(days=-num_in_week)
    timestamp = int(time.mktime(monday.timetuple()))
    return timestamp


def month_timestamp(num):
    """上个月第一天到上个月最后一天的持续时间，时间戳
    0: this month
    1: last month
    2: two month ago"""
    return get_month_timestamp(num)


# def week_market():
#     """市场部 本周 总销售额、销售冠军姓名、头像、销售额"""
#     cur = connect_postgresql()
#     timestamp = week_timestamp()
#
#     week_market_list = []
#
#     # cur.execute(
#     #     "select creator, sum(product_count * sell_price) as price from orders where deliver_time >%d and"
#     #     " product_id is not null group by creator order by price desc;" % timestamp)
#     cur.execute(
#         "select creator, sum(product_count * sell_price) as price from orders where deliver_time >%d"
#         "group by creator order by price desc;" % timestamp)
#
#     # cur.execute(
#     #     "select creator, sum(product_count * sell_price) as price from orders where deliver_time >%d and"
#     #     " product_id is not null group by creator order by price desc;" % 2505600)  # 2505600 for test
#
#     result_orders = cur.fetchall()
#     # print("result_orders=", result_orders)  # [('15625297106', 91688008.0), ('17180103332', 6000000.0)]
#
#     week_money, week_person_money, user_name, user_image = 0, 0, None, None
#     if result_orders:
#         # 周销售冠军
#         week_person_id = result_orders[0][0]
#         # 周销售冠军的销售额
#         week_person_money = result_orders[0][1]
#
#         for res in result_orders:
#             # 周销售总额
#             week_money += res[1]
#
#         cur.execute("select name, image from user_info where phone='%s';" % week_person_id)
#         result_user_info = cur.fetchall()
#         # print("result_user_info=", result_user_info)
#
#         if result_user_info:
#             user_name = result_user_info[0][0]
#             user_image = result_user_info[0][1]
#         else:
#             user_name, user_image = None, None
#
#     week_money = "%.2f" % round(week_money, 2)
#     week_money = "{:,}".format(week_money)
#     week_person_money = "%.2f" % round(week_person_money, 2)
#     week_person_money = "{:,}".format(week_person_money)
#
#     week_market_list.append(week_money)
#     week_market_list.append(week_person_money)
#     week_market_list.append(user_image)
#     week_market_list.append(user_name)
#
#     # print(week_market_list)
#     disconnect_postgresql(cur)
#     return week_market_list


# def two_month_ago_market():
#     """上上个月总销售额，用来和上个月销售额做对比"""
#     cur = connect_postgresql()
#
#     # 上上个月到上个月时间
#     now = datetime.datetime.now()
#     start = datetime.datetime(now.year, now.month - 2, 1)
#     end = datetime.datetime(now.year, now.month - 1, 1) - datetime.timedelta(seconds=1)
#     start_timestamp = int(time.mktime(start.timetuple()))
#     end_timestamp = int(time.mktime(end.timetuple()))
#
#     cur.execute(
#         "select creator, sum(product_count * sell_price) as price from orders where product_id is not null and"
#         " deliver_time between '%d' and '%d'  group by creator order by price desc;" % (start_timestamp, end_timestamp))
#
#     result_orders = cur.fetchall()
#     # print("result_orders=", result_orders)
#
#     two_month_ago_momey = 0
#     if result_orders:
#         for res in result_orders:
#             # 月销售总额
#             two_month_ago_momey += res[1]
#     # print("two_month_ago_momey=", two_month_ago_momey)
#
#     return two_month_ago_momey
#
#
# def month_market():
#     """市场部 上个月 总销售额、销售冠军姓名、头像、销售额"""
#     cur = connect_postgresql()
#     # 上个月第一天到最后一天时间
#     start_timestamp, end_timestamp = month_timestamp()
#
#     month_market_list = []
#
#     cur.execute(
#         "select creator, sum(product_count * sell_price) as price from orders where product_id is not null and"
#         " deliver_time between '%d' and '%d'  group by creator order by price desc;" % (start_timestamp, end_timestamp))
#     # cur.execute(
#     #     "select creator, sum(product_count * sell_price) as price from orders where product_id is not null"
#     #     " and deliver_time between '1541001600' and '1543507200'  group by creator order by price desc;")
#     result_orders = cur.fetchall()
#     # print("result_orders=", result_orders)  # [('15625297106', 91688008.0), ('17180103332', 6000000.0)]
#
#     month_money, month_person_money, user_name, user_image = 0, 0, None, None
#     if result_orders:
#         # 月销售冠军
#         month_person_id = result_orders[0][0]
#         # 月销售冠军的销售额
#         month_person_money = result_orders[0][1]
#
#         for res in result_orders:
#             # 月销售总额
#             month_money += res[1]
#
#         cur.execute("select name, image from user_info where phone='%s';" % month_person_id)
#         result_user_info = cur.fetchall()
#         # print("result_user_info=", result_user_info)
#
#         if result_user_info:
#             user_name = result_user_info[0][0]
#             user_image = result_user_info[0][1]
#         else:
#             user_name, user_image = None, None
#
#     two_month_ago_momey = two_month_ago_market()
#
#     if two_month_ago_momey != 0:
#         m_rose = (month_money - two_month_ago_momey) / month_money
#     else:
#         m_rose = 0
#     # print("m_rose=", m_rose)
#
#     month_money = "%.2f" % round(month_money, 2)
#     month_person_money = "%.2f" % round(month_person_money, 2)
#
#     month_market_list.append(month_money)
#     month_market_list.append(m_rose)
#     month_market_list.append(month_person_money)
#     month_market_list.append(user_image)
#     month_market_list.append(user_name)
#
#     # print(month_market_list)
#
#     return month_market_list


def week_product(factory_id):
    """生产部 本周产品出库 分类型号、名称、数量排名前3"""
    cur = connect_postgresql()
    timestamp = week_timestamp()  # 1545580800

    cur.execute(
        "select product_id, sum(count) from products_log where factory = '{}' and time > {} group by product_id having sum(count) < 0 "
        "order by sum(count) limit 3;".format(factory_id, timestamp))

    # cur.execute(
    #     "select product_id, sum(count) as co from products_log where time > {} group by product_id order by co limit 100;".format(
    #         1545580))

    result_products_log = cur.fetchall()
    # print("result_products_log=", result_products_log)

    week_product_list = []

    if result_products_log:
        for product in result_products_log:
            # print("product=", product)
            w_product = {}

            product_id = product[0] or None
            product_num = product[1] or 0

            w_product["count"] = abs(int(product_num))

            if product_id:
                cur.execute("select name, unit, category_id from products where id='{}';".format(product_id))
                result_products = cur.fetchall()  # [('一次性口罩', 9deSVx9iUzI0tSKuK8), ('急支糖浆', 9dGjrURmx6lfeZbedc)]
                # print("result_products=", result_products)  # [], [('保温杯', '个', '')], [('999感冒灵', '盒', '9dF9r7e8NDdGQU76jQ')]

                # if result_products:
                product_name = result_products[0][0] if result_products else ""
                product_unit = result_products[0][1] if result_products else ""
                product_category_id = result_products[0][2] if result_products else None
                # print("product_name=", product_name)  # 999感冒灵
                # print("product_unit=", product_unit)  # 盒
                # print("product_category_id=", product_category_id)  # '9dF9r7e8NDdGQU76jQ'
                w_product["name"] = product_name
                w_product["unit"] = product_unit

                if product_category_id:
                    cur.execute("select name from product_categories where id='{}'".format(product_category_id))
                    result_product_categories = cur.fetchall()
                    # print("result_product_categories=", result_product_categories)  # [('口服',)], [('外用',)]

                    product_category_name = result_product_categories[0][0] if result_product_categories else None
                    # print("product_category_name=", product_category_name)  # 口服

                    w_product["category_name"] = product_category_name
                else:
                    w_product["category_name"] = ""

            else:
                continue

            week_product_list.append(w_product)

    # print(week_product_list)
    disconnect_postgresql(cur)
    return week_product_list


def month_product(factory_id):
    """生产部 上个月产品出库 分类型号、名称、数量排名前3"""
    cur = connect_postgresql()
    start_timestamp, end_timestamp = month_timestamp(1)

    cur.execute(
        "select product_id, sum(count) from products_log where factory = '{}' and time between {} and {} group by product_id "
        "having sum(count) < 0 order by sum(count) limit 3;".format(factory_id, start_timestamp, end_timestamp))

    # for test
    # cur.execute(
    #     "select product_id, sum(count) from products_log where time between {} and {} group by product_id "
    #     "order by sum(count) limit 50;".format(15410, 1545804471))

    result_products_log = cur.fetchall()
    # print("result_products_log=", result_products_log)

    month_product_list = []

    if result_products_log:
        for product in result_products_log:
            # print("product=", product)
            m_product = {}

            product_id = product[0] or None
            product_num = product[1] or 0

            m_product["count"] = abs(int(product_num))

            if product_id:
                cur.execute("select name, unit, category_id from products where id='{}';".format(product_id))
                result_products = cur.fetchall()  # [('一次性口罩', 9deSVx9iUzI0tSKuK8), ('急支糖浆', 9dGjrURmx6lfeZbedc)]
                # print("result_products=",
                #       result_products)  # [], [('保温杯', '个', '')], [('999感冒灵', '盒', '9dF9r7e8NDdGQU76jQ')]

                # if result_products:
                product_name = result_products[0][0] if result_products else ""
                product_unit = result_products[0][1] if result_products else ""
                product_category_id = result_products[0][2] if result_products else None
                # print("product_name=", product_name)  # 999感冒灵
                # print("product_unit=", product_unit)  # 盒
                # print("product_category_id=", product_category_id)  # '9dF9r7e8NDdGQU76jQ'
                m_product["name"] = product_name
                m_product["unit"] = product_unit

                if product_category_id:
                    cur.execute("select name from product_categories where id='{}'".format(product_category_id))
                    result_product_categories = cur.fetchall()
                    # print("result_product_categories=", result_product_categories)  # [('口服',)], [('外用',)]

                    product_category_name = result_product_categories[0][0] if result_product_categories else None
                    # print("product_category_name=", product_category_name)  # 口服

                    m_product["category_name"] = product_category_name
                else:
                    m_product["category_name"] = ""

            else:
                continue

            month_product_list.append(m_product)

    disconnect_postgresql(cur)
    # print(month_product_list)
    return month_product_list


def week_store(factory_id):
    """仓库部 本周产品出库 分类型号、名称、数量排名前3"""
    cur = connect_postgresql()
    timestamp = week_timestamp()

    cur.execute(
        "select material_type_id, sum(material_count) from materials_log where factory = '{}' and time > {}"
        " group by material_type_id having sum(material_count) < 0 order by sum(material_count) limit 3;".format(
            factory_id, timestamp))

    result_materials_log = cur.fetchall()
    # print(result_materials_log)  # [('9dHV77G24bDzCvEBd2', -4.0), ('9dGvfekQT1KWZUcBEW', -2.0), ('9dGvdvuJhIfFDBQ4IK', -1.0)]

    week_store_list = []

    if result_materials_log:
        for material in result_materials_log:
            w_store = {}

            material_type_id = material[0] or None
            material_count = material[1] or 0

            w_store["count"] = abs(int(material_count))

            if material_type_id:
                cur.execute(
                    "select name, unit, category_id from material_types where id='{}';".format(material_type_id))
                result_material_types = cur.fetchall()

                # if result_material_types:
                name = result_material_types[0][0] if result_material_types else ""
                unit = result_material_types[0][1] if result_material_types else ""
                category_id = result_material_types[0][2] if result_material_types else None
                # print("name=", name)
                # print("unit=", unit)
                # print("category_id=", category_id)

                w_store["name"] = name
                w_store["unit"] = unit

                if category_id:
                    cur.execute("select name from material_categories where id='{}';".format(category_id))
                    result_material_categories = cur.fetchall()
                    # print("result_material_categories=", result_material_categories)  # [('电池材料',)]

                    category_name = result_material_categories[0][0] if result_material_categories else None
                    # print("category_name=", category_name)
                    w_store["category_name"] = category_name
                else:
                    w_store["category_name"] = ""

            else:
                continue

            week_store_list.append(w_store)

    # print("week_store_list=", week_store_list)
    disconnect_postgresql(cur)
    return week_store_list


def month_store(factory_id):
    """仓库部 上个月产品出库 分类型号、名称、数量排名前3"""
    cur = connect_postgresql()
    start_timestamp, end_timestamp = month_timestamp(1)

    cur.execute(
        "select material_type_id, sum(material_count) from materials_log where factory = '{}' and time between {} and {}"
        "group by material_type_id having sum(material_count) < 0 order by sum(material_count) limit 3;".format(
            factory_id, start_timestamp, end_timestamp))

    # for test
    # cur.execute("select material_type_id, sum(material_count) from materials_log where time between {} and {}"
    #             "group by material_type_id having sum(material_count) < 0 order by sum(material_count) limit 20;".format(
    #     start_timestamp, end_timestamp))

    result_materials_log = cur.fetchall()
    # print(result_materials_log)

    month_store_list = []

    if result_materials_log:
        for material in result_materials_log:
            m_store = {}

            material_type_id = material[0] or None
            material_count = material[1] or 0

            m_store["count"] = abs(int(material_count))

            if material_type_id:
                cur.execute(
                    "select name, unit, category_id from material_types where id='{}';".format(material_type_id))
                result_material_types = cur.fetchall()
                # print("result_material_types=", result_material_types)

                # if result_material_types:
                name = result_material_types[0][0] if result_material_types else ""
                unit = result_material_types[0][1] if result_material_types else ""
                category_id = result_material_types[0][2] if result_material_types else None

                m_store["name"] = name
                m_store["unit"] = unit

                if category_id:
                    cur.execute("select name from material_categories where id='{}';".format(category_id))
                    result_material_categories = cur.fetchall()
                    # print("result_material_categories=", result_material_categories)  # [('电池材料',)]

                    category_name = result_material_categories[0][0] if result_material_categories else ""
                    # print("category_name=", category_name)
                    m_store["category_name"] = category_name
                else:
                    m_store["category_name"] = ""

            else:
                continue

            month_store_list.append(m_store)

    # print("month_store_list=", month_store_list)  # [{'count': -1111}, {'count': -110}, {'count': -10}]
    disconnect_postgresql(cur)
    return month_store_list


def main(factory_id):
    """组装结果"""
    hzy = {}
    # ------仓库部------
    store = {}
    # 仓库部 本周产品出库
    week_store_list = week_store(factory_id)
    store["w"] = week_store_list

    # 仓库部 上个月产品出库
    month_store_list = month_store(factory_id)
    store["m"] = month_store_list

    hzy["store"] = store

    # ------生产部------
    product = {}

    # 生产部 本周产品出库
    week_product_list = week_product(factory_id)
    # 生产部 上个月产品出库
    month_product_list = month_product(factory_id)

    product["w"] = week_product_list
    product["m"] = month_product_list

    hzy["product"] = product
    # print("hzy=", hzy)
    return hzy


if __name__ == '__main__':
    main("")
