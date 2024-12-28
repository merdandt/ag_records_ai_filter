from openai import OpenAI
import streamlit as st
import sqlite3
import SQL.ddl as ddl

import LLM.prompts as pt

## If Using Google Generative Language API
client = OpenAI(
    api_key=st.secrets["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

## If Using OpenAI API
# client = OpenAI(
#     api_key = st.secrets["OPENAI_API_KEY"]
# )

# Function to get SQL from user question
def get_sql_from_text(user_question):
    completion = client.chat.completions.create(
        # If using OpenAI API
        # model="gpt-4o",
        # If using Google Generative Language API
        model="gemini-1.5-flash",
        temperature = 0,
        messages = [ 
            {"role": "system", "content": pt.SYSTEM_PROMPT.format(ddl=ddl.AGRECORD_DDL)},
            {
                "role": "user",
                "content": pt.USER_PROMPT.format(user_question=user_question)
            }
        ]
    )

    return completion.choices[0].message.content

# Function to retrieve query from database
def get_query_from_database(sql_query, db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql_query)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    print(data)

    return data

def clean_sql_code(sql):
    # Remove code block markers if present
    if sql.startswith("```"):
        sql = sql.strip('`')  # Remove leading and trailing backticks
        lines = sql.split('\n')
        # Remove language specifier if present
        if lines[0].lower() in ['sql', 'sql\n']:
            lines = lines[1:]
        sql = '\n'.join(lines)
    return sql.replace('```', '')