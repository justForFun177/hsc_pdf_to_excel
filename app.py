import time

import streamlit as st

import pdfplumber
import tabula
import pandas as pd

st.title("UPLOAD HSC RESULT PDF")
class PdDataFrame:
    def __init__(self):
        self.objs = {}

    def get_df(self, obj_name, header):
        if obj_name not in self.objs.keys():
            df_dict = {}
            for head in header:
                df_dict[head] = []
            self.objs[obj_name] = pd.DataFrame(df_dict)
        return self.objs[obj_name]

class HSCScienceParser:
    def __init__(self):
        self.df_obj = PdDataFrame()

    def parser_pdf(self, _file):
        with pdfplumber.open(_file) as pdf:
            # Iterate through each page of the PDF
            for page in pdf.pages:
                raw_data = page.extract_text()

                # Parse relevant information from the text
                head = raw_data.find('PUNE')
                NameIdx = raw_data.find('Name')
                MothernameIdx = raw_data.find('Mother')
                SeatNoIdx = raw_data.find('Seat No.')
                codeIdx = raw_data.find('Subject')
                totalmarkIdx = raw_data.find('TOTAL')
                PercentageIdx = raw_data.find('PERCENTAGE')
                resultIdx = raw_data.find('RESULT')

                HeadInfoInfo = raw_data[head:NameIdx]
                subject = raw_data[codeIdx:totalmarkIdx]
                subject = subject.strip()
                subjectlines = subject.splitlines()

                # Extract student marks group
                studentMarkGp = [subjectlines[i:i + 6] for i in range(1, len(subjectlines), 6)]

                # Extract individual marks
                result = []
                for string in subjectlines:
                    result.extend(string.split("  "))
                if '&' in result:
                    result.remove('&')

                TotalMarks = raw_data[PercentageIdx - len("1000"):PercentageIdx].strip()

    def do_parsing(self, input_file):
        try:
            df = tabula.read_pdf(input_file, pages="all", multiple_tables=True)
            temp = df[0]  # Assuming the first table is relevant
            parsed_df = temp[0:14].copy()

            # You can continue parsing the data using `self.parser_pdf(input_file)`
            # and handle the extracted data as needed.
            self.parser_pdf(input_file)

            return parsed_df

        except Exception as e:
            print(e)
            return None
try :
    pdf = st.file_uploader("UPLOAD A FILE")
    if pdf:
        parser = HSCScienceParser()
        parsed_df = parser.do_parsing(pdf)
    
        time.sleep(5)
        a = parsed_df.to_csv().encode('utf-8')
        st.download_button("DOWNLOAD FILE", a, file_name="final.csv", mime="text/csv")
except Exception:
    sr.error("PLEASE CHECK FILE FORMAT!!!")
