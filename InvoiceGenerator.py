from fpdf import FPDF
import csv
import pandas as pd

class PDF(FPDF):
    
    def print_order_info(self, order_info):
        self.set_font('Arial', '', 12)
        for info in order_info:
            if ':' in info:
               key, value = info.split(':', 1)
               key_cell_width = self.get_string_width(key + ':') + 2
               self.cell(key_cell_width , 10, key + ':', ln=False)
               self.set_font('Arial', 'B', 12)
               self.cell(0, 10, value, ln=True)
               self.set_font('Arial', '', 12)
            else:
               self.set_font('Arial', 'B', 12)
               self.cell(0, 10, info, ln=True)
               self.set_font('Arial', '', 12)

    def table_body(self, body):

       self.set_font('Arial', '', 12)
       col_widths = [max(self.get_string_width(str(entry.get(col, ''))) + 6, self.get_string_width(col) + 6) for entry in body for col in table_header]

    # table header
       self.set_font('Arial', 'B', 12)
       for col, width in zip(table_header, col_widths):
           self.cell(width, 10, col, 1)
       self.ln()

    # table data
       self.set_font('Arial', '', 12)
       total_value = 0
       for i, entry in enumerate(body, start=1):
            self.cell(col_widths[0], 10, str(i), 1)  # Add SNo column
            for col, width in zip(selected_columns, col_widths[1:]):
                value = entry.get(col, '')
                self.cell(width, 10, str(value), 1)

                if col == "SALES":
                    total_value += float(value)
            self.ln()
       self.set_font('Arial', 'B', 12)
       self.cell(col_widths[0], 10, "", 1)  # Empty cell for SNo
       for col, width in zip(selected_columns, col_widths[1:]):
              if col == "PRICEEACH":
                    self.cell(width, 10, "Total $", 1)
              elif col == "SALES":
                  self.cell(width, 10, f'{total_value:.2f}', 1)
              else:
                  self.cell(width, 10, "", 1)
       self.ln()

    
def read_csv_data(csv_file, selected_columns, order):
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [
            {col: row.get(col, '') for col in selected_columns}
            for row in reader
            if row.get('ORDERNUMBER') == order
        ]
    return data

if __name__ == "__main__":
    my_file= r"D:\PythonCode\AutoSalesData.csv"
    order=input('Enter the order number:\n')
    pdf = PDF()
    pdf.add_page()

    pdf.set_font('Arial', '', 12)
    orderno_info_col = ['ORDERNUMBER', 'ORDERDATE', 'CUSTOMERNAME', 'ADDRESSLINE1','CITY', 'POSTALCODE', 'COUNTRY', 'PHONE', 'CONTACTFIRSTNAME', 'CONTACTLASTNAME']

    order_info_data = read_csv_data(my_file, orderno_info_col , order)
    order_info = [
        f'Sale Order #: {order_info_data[0].get("ORDERNUMBER", "")}',
        f'Order Date: {order_info_data[0].get("ORDERDATE", "")}',
        f'Customer: {order_info_data[0].get("CUSTOMERNAME", "")}',
        'Shipping Address:',
        f'{order_info_data[0].get("ADDRESSLINE1", "")},',
        f'{order_info_data[0].get("CITY", "")}-{order_info_data[0].get("POSTALCODE", "")},',
        order_info_data[0].get("COUNTRY", ""),
        f'Phone: {order_info_data[0].get("PHONE", "")}',
        f'Contact: {order_info_data[0].get("CONTACTFIRSTNAME", "")} {order_info_data[0].get("CONTACTLASTNAME", "")}',
    ]
    pdf.print_order_info(order_info)
    table_header=['S.N','Product Code', 'Product Line', 'Qty' , 'Price $' , 'Value $']
    selected_columns = ['PRODUCTCODE', 'PRODUCTLINE', 'QUANTITYORDERED' , 'PRICEEACH' , 'SALES']
    table_data = read_csv_data(my_file, selected_columns, order)
    pdf.table_body(table_data)
    pdf.output("invoice.pdf")