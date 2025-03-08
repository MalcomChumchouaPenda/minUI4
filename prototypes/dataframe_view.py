
import sys
import context
import pandas as pd
from PyQt4.QtGui import QApplication
from minui4.widgets.dataframe_view import DataFrameView


app = QApplication(sys.argv)
df = pd.DataFrame({
    'Nom': ['Alice', 'Bob', 'Charlie'],
    'Âge': [25, 30, 35],
    'Ville': ['Paris', 'Lyon', 'Marseille']
})

window = DataFrameView(df)
window.setWindowTitle("DataFrameView avec Édition")
window.resize(500, 400)
window.show()

sys.exit(app.exec_())