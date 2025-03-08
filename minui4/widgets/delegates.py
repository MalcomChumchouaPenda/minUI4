from PyQt4.QtCore import Qt, QDate, QTime, QDateTime
from PyQt4.QtGui import QStyledItemDelegate, QDateEdit, QTimeEdit, QDateTimeEdit


class DateDelegate(QStyledItemDelegate):
    """Délégué pour éditer des dates."""
    
    def createEditor(self, parent, option, index):
        editor = QDateEdit(parent)
        editor.setCalendarPopup(True)  # Permet d'ouvrir un calendrier pour sélectionner une date
        editor.setDisplayFormat("yyyy-MM-dd")
        return editor

    def setEditorData(self, editor, index):
        date_str = index.model().data(index, Qt.DisplayRole)
        if date_str:
            editor.setDate(QDate.fromString(date_str, "yyyy-MM-dd"))

    def setModelData(self, editor, model, index):
        print('called', index, editor.date())
        model.setData(index, editor.date().toString("yyyy-MM-dd"), Qt.EditRole)
        print(model._dataframe)


class TimeDelegate(QStyledItemDelegate):
    """Délégué pour éditer des heures."""
    
    def createEditor(self, parent, option, index):
        editor = QTimeEdit(parent)
        editor.setDisplayFormat("HH:mm:ss")
        return editor

    def setEditorData(self, editor, index):
        time_str = index.model().data(index, Qt.DisplayRole)
        if time_str:
            editor.setTime(QTime.fromString(time_str, "HH:mm:ss"))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.time().toString("HH:mm:ss"), Qt.EditRole)


class DateTimeDelegate(QStyledItemDelegate):
    """Délégué pour éditer des datetime."""
    
    def createEditor(self, parent, option, index):
        editor = QDateTimeEdit(parent)
        editor.setCalendarPopup(True)
        editor.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        return editor

    def setEditorData(self, editor, index):
        datetime_str = index.model().data(index, Qt.DisplayRole)
        if datetime_str:
            editor.setDateTime(QDateTime.fromString(datetime_str, "yyyy-MM-dd HH:mm:ss"))

    def setModelData(self, editor, model, index):
        print('called', index, editor.date())
        model.setData(index, editor.dateTime().toString("yyyy-MM-dd HH:mm:ss"), Qt.EditRole)
        print(model._dataframe)
        print(model._dataframe.dtypes)
