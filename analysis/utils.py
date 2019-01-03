# -*- coding: utf-8 -*-
import psycopg2
import os

database = os.environ.get("PG_DATABASE") or "db_dsdapp"
user = os.environ.get("PG_USER") or "dsd"
password = os.environ.get("PG_PASSWORD") or "dsdPassword"
host = os.environ.get("PG_HOST") or "120.77.221.233"
port = os.environ.get("PG_PORT") or "5432"


def connect_postgresql():
    """连接数据库"""
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    return cur


def disconnect_postgresql(cur):
    """关闭游标"""
    cur.close()
