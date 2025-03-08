
import sys
import context
import pandas as pd
from PyQt4.QtGui import QApplication
from minui4.widgets.dataframe_view import DataFrameView


app = QApplication(sys.argv)
df = pd.DataFrame({
    'DateNaissance': [pd.Timestamp('1995-06-15').date(), pd.Timestamp('1988-09-23').date(), pd.Timestamp('2000-12-05').date()],
    'HeureRDV': [pd.Timestamp('10:30:00').time(), pd.Timestamp('14:45:00').time(), pd.Timestamp('09:15:00').time()],
    'DerniereConnexion': [pd.Timestamp('2024-02-25 12:00:00'), pd.Timestamp('2024-02-26 08:45:00'), pd.Timestamp('2024-02-27 22:30:00')]
})

window = DataFrameView(df)
window.setWindowTitle("DataFrameView avec Dates")
window.resize(500, 400)
window.show()

sys.exit(app.exec_())