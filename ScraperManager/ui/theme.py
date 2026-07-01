DARK_THEME = """
QMainWindow {
    background-color: #1E1E1E;
}

QWidget {
    background-color: #1E1E1E;
    color: #F2F2F2;
    font-family: "Segoe UI";
    font-size: 13px;
}

QGroupBox {
    border: 1px solid #3A3A3A;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
    color: #FFFFFF;
}

QTabWidget::pane {
    border: 1px solid #3A3A3A;
    background: #252526;
    border-radius: 8px;
}

QTabBar::tab {
    background: #2D2D30;
    color: #CCCCCC;
    padding: 10px 18px;
    margin: 2px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

QTabBar::tab:selected {
    background: #007ACC;
    color: white;
    font-weight: bold;
}

QTabBar::tab:hover {
    background: #3A3D41;
}

QLineEdit,
QTextEdit,
QPlainTextEdit,
QComboBox,
QSpinBox,
QDoubleSpinBox {
    background-color: #2A2D2E;
    color: white;
    border: 1px solid #444;
    border-radius: 6px;
    padding: 6px;
    selection-background-color: #007ACC;
}

QLineEdit:focus,
QTextEdit:focus,
QPlainTextEdit:focus,
QComboBox:focus {
    border: 1px solid #0099FF;
}

QPushButton {
    background-color: #007ACC;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1493FF;
}

QPushButton:pressed {
    background-color: #005A9E;
}

QPushButton:disabled {
    background-color: #3A3A3A;
    color: #888;
}

QTableWidget {
    background-color: #252526;
    color: #F2F2F2;
    alternate-background-color: #2D2D30;
    gridline-color: #3A3A3A;
    border: 1px solid #3A3A3A;
    selection-background-color: #007ACC;
    selection-color: white;
}

QTableCornerButton::section {
    background: #2D2D30;
    border: none;
}

QHeaderView::section {
    background-color: #2D2D30;
    color: white;
    padding: 8px;
    border: none;
    font-weight: bold;
}

QListWidget {
    background-color: #252526;
    border: 1px solid #3A3A3A;
    border-radius: 6px;
}

QListWidget::item {
    padding: 6px;
}

QListWidget::item:selected {
    background: #007ACC;
    color: white;
}

QScrollBar:vertical {
    background: #202020;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #5A5A5A;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #777777;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QStatusBar {
    background: #252526;
    color: #CCCCCC;
}

QMenuBar {
    background: #252526;
    color: white;
}

QMenuBar::item:selected {
    background: #007ACC;
}

QMenu {
    background: #2D2D30;
    color: white;
}

QMenu::item:selected {
    background: #007ACC;
}
"""