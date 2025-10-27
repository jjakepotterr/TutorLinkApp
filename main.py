import search.py
import streamlit as st
from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route('/') #set server home address
def greeter():
    return '<p>Its over 4 us<p>'
