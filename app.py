import streamlit as st
import sqlite3
import pandas as pd


def init_db():
    conn = sqlite3.connect("specimens.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS specimens (
                username TEXT,
                specimen_size REAL,
                actual_size REAL)''')

    conn.commit()
    conn.close()

def save_to_db(username, specimen_size, actual_size):
    conn = sqlite3.connect("specimens.db")
    c = conn.cursor()
    c.execute("INSERT INTO specimens VALUES (?, ?, ?)",
              (username, specimen_size, actual_size))
    conn.commit()
    conn.close() 




def calculate_real_life_size(microscope_size, magnification):
    return microscope_size / magnification


def main():
    st.set_page_config(page_title="Microscope Size Calculator")
    st.title("Microscope Size to Real-Life Size Calculator")

    init_db()

    with st.form("size_form"):
        username = st.text_input("Enter your name")
        microscope_size = st.number_input("Microscope size (µm)", min_value=0.0, format="%.2f")
        magnification = st.number_input("Magnification", min_value=1.0, format="%.2f")
        submitted = st.form_submit_button("Calculate and Save")

        if submitted:
            if username.strip() == "":
                st.warning("Please enter your name.")
            elif magnification == 0:
                st.warning("Magnification cannot be zero.")
            else:
                real_size = calculate_real_life_size(microscope_size, magnification)
                save_to_db(username, microscope_size, real_size)
                st.success(f"Real-life size: {real_size:.2f} µm saved successfully!")

    if st.checkbox("Show all saved records"):
        conn = sqlite3.connect("specimens.db")
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM specimens").fetchall()
        conn.close()

        if rows:
            df = pd.DataFrame(rows, columns=["Username", "Specimen Size (µm)", "Actual Size (µm)"])
            st.table(df)
        else:
            st.info("No records found yet.")

if __name__ == "__main__":
    main()
