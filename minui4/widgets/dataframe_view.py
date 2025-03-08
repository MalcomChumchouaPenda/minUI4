import numpy as np
import pandas as pd
from PyQt4.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt4.QtGui import QApplication, QTableView, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QInputDialog, QMessageBox
from .delegates import DateDelegate, TimeDelegate, DateTimeDelegate


class DataFrameView(QWidget):

    def __init__(self, dataframe=None, parent=None):
        super(DataFrameView, self).__init__(parent)
        self.table_view = QTableView(self)
        self.table_model = DataFrameModel(dataframe if dataframe is not None else pd.DataFrame(), self)
        self.table_view.setModel(self.table_model)

        # Définir les délégués pour la gestion des types
        for col, dtype in dataframe.dtypes.items():
            col_idx = dataframe.columns.get_loc(col)
            if dtype == 'datetime64[ns]':
                self.table_view.setItemDelegateForColumn(col_idx, DateTimeDelegate(self))
            elif dtype == 'object' and dataframe[col].astype(str).str.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$').all():
                self.table_view.setItemDelegateForColumn(col_idx, DateTimeDelegate(self))
            elif dtype == 'object' and dataframe[col].astype(str).str.match(r'^\d{4}-\d{2}-\d{2}$').all():
                self.table_view.setItemDelegateForColumn(col_idx, DateDelegate(self))
            elif dtype == 'object' and dataframe[col].astype(str).str.match(r'^\d{2}:\d{2}:\d{2}$').all():
                self.table_view.setItemDelegateForColumn(col_idx, TimeDelegate(self))

        # Boutons pour l'édition des données
        self.add_button = QPushButton("Ajouter ligne")
        self.delete_button = QPushButton("Supprimer ligne")
        self.edit_button = QPushButton("Modifier cellule")

        # Layout pour les boutons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.edit_button)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_view)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Connexion des boutons
        self.add_button.clicked.connect(self.add_row)
        self.delete_button.clicked.connect(self.delete_row)
        self.edit_button.clicked.connect(self.edit_cell)

    def model(self):
        return self.table_model  # Permet aux tests d'accéder au modèle

    def add_row(self):
        """Ajoute une ligne vide."""
        self.table_model.insertRows(self.table_model.rowCount(), 1)

    def delete_row(self):
        """Supprime la ligne sélectionnée."""
        index = self.table_view.currentIndex()
        if index.isValid():
            self.table_model.removeRows(index.row(), 1)

    def delete_row(self):
        """Supprime la ligne sélectionnée après confirmation."""
        index = self.table_view.currentIndex()
        if index.isValid():
            reply = QMessageBox.question(self, 'Confirmer', 
                                         "Êtes-vous sûr de vouloir supprimer cette ligne ?",
                                         QMessageBox.Yes | QMessageBox.No, 
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.table_model.removeRows(index.row(), 1)
        else:
            QMessageBox.warning(self, 'Erreur', 'Aucune ligne sélectionnée pour suppression.')

    def edit_cell(self):
        """Modifie la cellule sélectionnée."""
        index = self.table_view.currentIndex()
        if index.isValid():
            current_value = self.table_model.data(index, Qt.DisplayRole)
            new_value, ok = QInputDialog.getText(self, "Modifier Cellule", "Nouvelle valeur:", text=current_value)
            if ok:
                self.table_model.setData(index, new_value, Qt.EditRole)


    def copy_selection(self):
        """Copie la valeur de la cellule sélectionnée dans le presse-papiers."""
        index = self.table_view.currentIndex()
        if index.isValid():
            value = self.model().data(index, Qt.DisplayRole)
            QApplication.clipboard().setText(value)

    def cut_selection(self):
        """Coupe la valeur de la cellule sélectionnée (copie puis supprime)."""
        index = self.table_view.currentIndex()
        if index.isValid():
            value = self.model().data(index, Qt.DisplayRole)
            QApplication.clipboard().setText(value)
            self.model().setData(index, "", Qt.EditRole)

    def paste_selection(self):
        """Colle la valeur du presse-papiers dans la cellule sélectionnée en respectant le type de la colonne."""
        index = self.table_view.currentIndex()
        if not index.isValid():
            return
        
        try:
            clipboard_value = QApplication.clipboard().text()
            self.model().setData(index, clipboard_value, Qt.EditRole)
        
        except ValueError:
            msg = "Impossible de coller '%s' dans la colonne %s." % (clipboard_value, index.column())
            QMessageBox.warning(self, "Erreur de collage", msg)
            

class DataFrameModel(QAbstractTableModel):

    def __init__(self, dataframe=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self._dataframe = dataframe
        print(dataframe.dtypes)

    def rowCount(self, parent=None):
        return self._dataframe.shape[0]

    def columnCount(self, parent=None):
        return self._dataframe.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return 
        
        value = self._dataframe.iloc[index.row(), index.column()]        
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return str(value)
        return

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole:
            return False
        
        # Obtenir le type de la colonne
        column_name = self._dataframe.columns[index.column()]
        column_dtype = self._dataframe[column_name].dtype

        # Convertir la valeur collée en fonction du type attendu
        if column_dtype == "int64":
            if value is None or value == '':
                converted_value = 0
            else:
                converted_value = int(value)
        elif column_dtype == "float64":
            converted_value = float(value)
        elif column_dtype == "bool":
            converted_value = value.lower() in ["true", "1", "yes"]
        elif column_dtype == "datetime64[ns]":
            converted_value = pd.to_datetime(value)
        elif column_dtype == "timedelta64[ns]":
            converted_value = pd.to_timedelta(value)
        # elif column_dtype == "category":
        #     converted_value = value if value in self._dataframe[column_name].cat.categories else None
        else:
            converted_value = value  # Texte par défaut

        if converted_value is None:
            converted_value = np.nan
            # raise ValueError("Valeur collée invalide pour cette colonne.")
            
        # Mise à jour du DataFrame
        self._dataframe.at[index.row(), column_name] = converted_value
        self.dataChanged.emit(index, index)  # Notifie la vue du changement
        return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return
        
        if orientation == Qt.Horizontal:
            return self._dataframe.columns[section]
        elif orientation == Qt.Vertical:
            return str(section)
        return

    def flags(self, index):
        """Permet l'édition des cellules."""
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def insertRows(self, row, count, parent=None):
        """Insère `count` lignes à partir de `row`."""
        self.beginInsertRows(parent or QModelIndex(), row, row + count - 1)

        for _ in range(count):
            new_row = {col: "" for col in self._dataframe.columns}
            self._dataframe = pd.concat([self._dataframe.iloc[:row], pd.DataFrame([new_row]), self._dataframe.iloc[row:]]).reset_index(drop=True)

        self.endInsertRows()
        return True

    def removeRows(self, row, count, parent=None):
        """Supprime `count` lignes à partir de `row`."""
        if row < 0 or row + count > self.rowCount():
            return False
        
        self.beginRemoveRows(parent or QModelIndex(), row, row + count - 1)
        self._dataframe.drop(self._dataframe.index[row:row+count], inplace=True)
        self._dataframe.reset_index(drop=True, inplace=True)
        self.endRemoveRows()
        return True

