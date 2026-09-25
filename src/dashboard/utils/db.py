import sqlite3
import pandas as pd
import streamlit as st
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "nifty100.db")

if not os.path.exists(DB_PATH):
    ALT_PATH = os.path.join(os.getcwd(), "data", "nifty100.db")
    if os.path.exists(ALT_PATH):
        DB_PATH = ALT_PATH

def get_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database file not found at: {DB_PATH}")
    return sqlite3.connect(DB_PATH)

@st.cache_data(ttl=600)
def get_companies():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM companies", conn)
    conn.close()
    return df

@st.cache_data(ttl=600)
def get_ratios(ticker=None, year=None):
    conn = get_connection()
    query = "SELECT * FROM financial_ratios WHERE 1=1"
    params = []
    if ticker:
        query += " AND (company_id = ? OR ticker = ?)"
        params.extend([ticker, ticker])
    if year:
        query += " AND year = ?"
        params.append(year)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

@st.cache_data(ttl=600)
def get_pl(ticker):
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM profit_loss WHERE company_id = ?", conn, params=[ticker])
    conn.close()
    return df

@st.cache_data(ttl=600)
def get_bs(ticker):
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM balance_sheet WHERE company_id = ?", conn, params=[ticker])
    conn.close()
    return df

@st.cache_data(ttl=600)
def get_cf(ticker):
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM cash_flow WHERE company_id = ?", conn, params=[ticker])
    conn.close()
    return df

@st.cache_data(ttl=600)
def get_sectors():
    conn = get_connection()
    df = pd.read_sql_query("SELECT DISTINCT broad_sector FROM companies", conn)
    conn.close()
    return df['broad_sector'].dropna().tolist()

@st.cache_data(ttl=600)
def get_peers(group_name):
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM peer_comparison WHERE group_name = ?", conn, params=[group_name])
    conn.close()
    return df

@st.cache_data(ttl=600)
def get_valuation(ticker=None):
    conn = get_connection()
    query = "SELECT * FROM valuation"
    params = []
    if ticker:
        query += " WHERE company_id = ?"
        params.append(ticker)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df
