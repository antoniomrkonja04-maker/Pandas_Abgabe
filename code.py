import streamlit as st
import pandas as pd

datei = "data/activity.csv"

df = pd.read_csv(datei)

print (df.head())
