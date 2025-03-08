from unittest import mock
import pytest
import pandas as pd
from PyQt4.QtCore import Qt, QDate, QTime, QDateTime
from PyQt4.QtGui import QApplication
from minui4.widgets.dataframe_view import DataFrameView, DataFrameModel


@pytest.fixture
def sample_df1():
    """Fixture pour fournir un DataFrame de test."""
    return pd.DataFrame({
        'Nom': ['Alice', 'Bob', 'Charlie'],
        'Âge': [25, 30, 35],
        'Ville': ['Paris', 'Lyon', 'Marseille']
    })

@pytest.fixture
def df_view1(qtbot, sample_df1):
    """Fixture pour initialiser le widget DataFrameView avec un DataFrame de test."""
    widget = DataFrameView(sample_df1)
    qtbot.addWidget(widget)
    return widget

def test_view_initialization(df_view1, sample_df1):
    """Vérifie que le widget est bien initialisé avec le bon nombre de lignes et colonnes."""
    model = df_view1.model()
    assert model.rowCount() == len(sample_df1)
    assert model.columnCount() == len(sample_df1.columns)

def test_view_data_retrieval(df_view1, sample_df1):
    """Vérifie que les valeurs du modèle correspondent à celles du DataFrame."""
    model = df_view1.model()
    for row in range(model.rowCount()):
        for col in range(model.columnCount()):
            expected_value = sample_df1.iloc[row, col]
            index = model.index(row, col)
            assert model.data(index, Qt.DisplayRole) == str(expected_value)

def test_view_edit_data(qtbot, df_view1):
    """Simule la modification d'une cellule et vérifie que le DataFrame est mis à jour."""
    model = df_view1.model()
    index = model.index(1, 1)  # Modification de l'âge de "Bob"
    new_value = "32"
    
    assert model.setData(index, new_value, Qt.EditRole)  # Vérifie que la modification est acceptée
    assert model.data(index, Qt.DisplayRole) == new_value  # Vérifie que la modification est visible


@pytest.fixture
def sample_df2():
    """Crée un DataFrame de test."""
    return pd.DataFrame({
        'Nom': ['Alice', 'Bob'],
        'Âge': [25, 30]
    })

@pytest.fixture
def df_model2(sample_df2, qtbot):
    """Crée une instance du modèle avec le DataFrame de test."""
    model = DataFrameModel(sample_df2)
    return model

def test_insert_row(df_model2, qtbot):
    """Teste l'insertion d'une nouvelle ligne."""
    nrow = df_model2.rowCount()
    with qtbot.waitSignal(df_model2.rowsInserted, timeout=500):
        df_model2.insertRows(nrow, 1)

    assert df_model2.rowCount() == nrow + 1
    assert all(df_model2._dataframe.iloc[-1] == "")  # Vérifie que la nouvelle ligne est vide

def test_remove_row(df_model2, qtbot):
    """Teste la suppression d'une ligne."""
    nrow = df_model2.rowCount()
    with qtbot.waitSignal(df_model2.rowsRemoved, timeout=500):
        df_model2.removeRows(0, 1)

    assert df_model2.rowCount() == nrow - 1
    assert "Alice" not in df_model2._dataframe['Nom'].values  # Vérifie que la première ligne a bien été supprimée

def test_insert_multiple_rows(df_model2, qtbot):
    """Teste l'insertion de plusieurs lignes."""
    nrow = df_model2.rowCount()
    with qtbot.waitSignal(df_model2.rowsInserted, timeout=500):
        df_model2.insertRows(nrow, 3)

    assert df_model2.rowCount() == nrow + 3
    assert all(df_model2._dataframe.iloc[-1] == "")  # Vérifie que les nouvelles lignes sont vides

def test_remove_multiple_rows(df_model2, qtbot):
    """Teste la suppression de plusieurs lignes."""
    nrow = df_model2.rowCount()
    with qtbot.waitSignal(df_model2.rowsRemoved, timeout=500):
        df_model2.removeRows(0, min(2, nrow))  # Supprime les deux premières lignes

    assert df_model2.rowCount() == max(0, nrow - 2)
    assert "Alice" not in df_model2._dataframe['Nom'].values
    assert "Bob" not in df_model2._dataframe['Nom'].values if nrow > 1 else True


@pytest.fixture
def sample_df3():
    return pd.DataFrame({
        'DateX': ['2025-02-25', '2025-03-01'],
        'TimeX': ['12:30:45', '08:15:00'],
        'DateTimeX': ['2025-02-25 12:30:45', '2025-03-01 08:15:00'],
        'DateY': [pd.Timestamp('2025-02-25').date(), pd.Timestamp('2025-03-01').date()],
        'TimeY': [pd.Timestamp('12:30:45').time(), pd.Timestamp('08:15:00').time()],
        'DateTimeY': [pd.Timestamp('2025-02-25 12:30:45'), pd.Timestamp('2025-03-01 08:15:00')]
    })

@pytest.fixture
def df_view3(qtbot, sample_df3):
    """Instancie DataFrameView avec des données de test."""
    widget = DataFrameView(sample_df3)
    qtbot.addWidget(widget)
    # widget.show()
    return widget

@pytest.fixture
def df_model3(sample_df3, qtbot):
    """Fixture qui crée un modèle de données basé sur un DataFrame avec des dates."""
    model = DataFrameModel(sample_df3)
    return model

@pytest.mark.parametrize("colname", ['DateX', 'DateY'])
def test_detect_dtype_and_create_date_delegate(df_view3, sample_df3, colname):
    """Teste la bonne utilisation du delegate pour la colonne Date."""
    table = df_view3.table_view
    col = sample_df3.columns.get_loc(colname)
    delegate = table.itemDelegateForColumn(col)  # Colonne "Date"
    assert delegate is not None, "Aucun ItemDelegate trouvé pour la colonne Date."

@pytest.mark.parametrize("colname", ['TimeX', 'TimeY'])
def test_detect_dtype_and_create_time_delegate(df_view3, sample_df3, colname):
    """Teste la bonne utilisation du delegate pour la colonne Time."""
    table = df_view3.table_view
    col = sample_df3.columns.get_loc(colname)
    delegate = table.itemDelegateForColumn(col)  # Colonne "Time"
    assert delegate is not None, "Aucun ItemDelegate trouvé pour la colonne Time."

@pytest.mark.parametrize("colname", ['DateTimeX', 'DateTimeY'])
def test_detect_dtype_and_create_datetime_delegate(df_view3, sample_df3, colname):
    """Teste la bonne utilisation du delegate pour la colonne DateTime."""
    table = df_view3.table_view
    col = sample_df3.columns.get_loc(colname)
    delegate = table.itemDelegateForColumn(col)  # Colonne "DateTime"
    assert delegate is not None, "Aucun ItemDelegate trouvé pour la colonne DateTime."


@pytest.mark.parametrize("colname", ['DateX', 'DateY'])
def test_get_inner_value_with_date_delegate(df_view3, sample_df3, colname):
    table = df_view3.table_view
    col = sample_df3.columns.get_loc(colname)
    delegate = table.itemDelegateForColumn(col)  # Colonne "Date"

    index = table.model().index(0, col)
    editor = delegate.createEditor(table, None, index)
    delegate.setEditorData(editor, index)
    assert editor.date() == QDate(2025, 2, 25)

@pytest.mark.parametrize("colname", ['TimeX', 'TimeY'])
def test_get_inner_value_with_time_delegate(df_view3, sample_df3, colname):
    table = df_view3.table_view
    col = sample_df3.columns.get_loc(colname)
    delegate = table.itemDelegateForColumn(col)  # Colonne "Time"

    index = table.model().index(0, col)
    editor = delegate.createEditor(table, None, index)
    delegate.setEditorData(editor, index)
    assert editor.time() == QTime(12, 30, 45)

@pytest.mark.parametrize("colname", ['DateTimeX', 'DateTimeY'])
def test_get_inner_value_with_datetime_delegate(df_view3, sample_df3, colname):
    table = df_view3.table_view
    col = sample_df3.columns.get_loc(colname)
    delegate = table.itemDelegateForColumn(col)  # Colonne "DateTime"

    index = table.model().index(0, col)
    editor = delegate.createEditor(table, None, index)
    delegate.setEditorData(editor, index)
    assert editor.dateTime() == QDateTime(2025, 2, 25, 12, 30, 45)


@pytest.mark.parametrize("colname", ['DateX', 'DateY'])
def test_display_date_values(df_model3, sample_df3, colname):
    """Teste si les valeurs des dates sont correctement affichées sous forme de chaîne de caractères."""
    col = sample_df3.columns.get_loc(colname)
    index = df_model3.index(0, col)
    assert df_model3.data(index, Qt.DisplayRole) == "2025-02-25"

@pytest.mark.parametrize("colname", ['TimeX', 'TimeY'])
def test_display_time_values(df_model3, sample_df3, colname):
    """Teste si les valeurs des times sont correctement affichées sous forme de chaîne de caractères."""
    col = sample_df3.columns.get_loc(colname)
    index = df_model3.index(1, col)
    assert df_model3.data(index, Qt.DisplayRole) == "08:15:00"

@pytest.mark.parametrize("colname", ['DateTimeX', 'DateTimeY'])
def test_display_datetime_values(df_model3, sample_df3, colname):
    """Teste si les valeurs des datetimes sont correctement affichées sous forme de chaîne de caractères."""
    col = sample_df3.columns.get_loc(colname)
    index = df_model3.index(1, col) 
    assert df_model3.data(index, Qt.DisplayRole) == "2025-03-01 08:15:00"


@pytest.mark.parametrize("colname", ['DateX', 'DateY'])
def test_edit_value_with_date_delegate(df_view3, sample_df3, colname):
    table = df_view3.table_view
    col = sample_df3.columns.get_loc(colname)
    delegate = table.itemDelegateForColumn(col)                # Colonne "Date"

    index = table.model().index(0, col)
    editor = delegate.createEditor(table, None, index)
    editor.setDate(QDate(2030, 1, 1))                          # Modifier la date et l'heure
    delegate.setModelData(editor, table.model(), index)
    assert table.model().data(index, Qt.DisplayRole) == "2030-01-01"

@pytest.mark.parametrize("colname", ['TimeX', 'TimeY'])
def test_edit_value_with_time_delegate(df_view3, sample_df3, colname):
    table = df_view3.table_view
    col = sample_df3.columns.get_loc(colname)
    delegate = table.itemDelegateForColumn(col)                # Colonne "Time"

    index = table.model().index(0, col)
    editor = delegate.createEditor(table, None, index)
    editor.setTime(QTime(23, 59, 59))                          # Modifier la date et l'heure
    delegate.setModelData(editor, table.model(), index)
    assert table.model().data(index, Qt.DisplayRole) == "23:59:59"

@pytest.mark.parametrize("colname", ['DateTimeX', 'DateTimeY'])
def test_edit_value_with_datetime_delegate(df_view3, sample_df3, colname):
    table = df_view3.table_view
    col = sample_df3.columns.get_loc(colname)
    delegate = table.itemDelegateForColumn(col)                 # Colonne "DateTime"

    index = table.model().index(0, col)
    editor = delegate.createEditor(table, None, index)
    editor.setDateTime(QDateTime(2030, 12, 31, 23, 59, 59))     # Modifier la date et l'heure
    delegate.setModelData(editor, table.model(), index)
    assert table.model().data(index, Qt.DisplayRole) == "2030-12-31 23:59:59"


@pytest.fixture
def sample_df4():
    """Crée un DataFrame de test."""
    return pd.DataFrame({
        'Nom': ['Alice', 'Bob', 'Charlie'],
        'Âge': [25, 30, 35],
        'Ville': ['Paris', 'Lyon', 'Marseille']
    })

@pytest.fixture
def df_view4(qtbot, sample_df4):
    """Instancie DataFrameView et l'ajoute à QtBot."""
    widget = DataFrameView(sample_df4)
    qtbot.addWidget(widget)
    widget.show()
    return widget

def test_copy_selection(df_view4, sample_df4):
    """Teste la copie d'une cellule sélectionnée."""
    table = df_view4.table_view
    model = df_view4.model()
    clipboard = QApplication.clipboard()

    # Sélectionner une cellule (ex: Nom de Bob)
    col = sample_df4.columns.get_loc('Nom')
    index = model.index(1, col)
    table.setCurrentIndex(index)

    # Copier
    df_view4.copy_selection()

    # Vérifier que le presse-papiers contient bien la valeur copiée
    assert clipboard.text() == "Bob"

def test_cut_selection(df_view4, sample_df4):
    """Teste le couper d'une cellule sélectionnée."""
    table = df_view4.table_view
    model = df_view4.model()
    clipboard = QApplication.clipboard()

    # Sélectionner une cellule (ex: Ville de Charlie)
    col = sample_df4.columns.get_loc('Ville')
    index = model.index(2, col)
    table.setCurrentIndex(index)

    # Couper
    df_view4.cut_selection()

    # Vérifier que le presse-papiers contient la valeur coupée
    assert clipboard.text() == "Marseille"

    # Vérifier que la cellule est maintenant vide
    assert model.data(index, Qt.DisplayRole) == ""

def test_paste_selection(df_view4, sample_df4):
    """Teste le collage d'une valeur copiée."""
    table = df_view4.table_view
    model = df_view4.model()
    clipboard = QApplication.clipboard()

    # Copier une valeur (ex: "Lyon")
    clipboard.setText("Lyon")

    # Sélectionner une autre cellule (ex: Nom de Charlie)
    col = sample_df4.columns.get_loc('Nom')
    index = model.index(2, col)
    table.setCurrentIndex(index)

    # Coller
    df_view4.paste_selection()

    # Vérifier que la valeur a bien été collée
    assert model.data(index, Qt.DisplayRole) == "Lyon"    
