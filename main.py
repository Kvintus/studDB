from flask import Flask, flash, redirect, render_template, request, session, url_for
from cs50 import SQL


app = Flask(__name__)
db = SQL("sqlite:///assets/databaza.db")
