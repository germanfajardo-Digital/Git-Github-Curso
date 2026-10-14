import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class TextFileEditor(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.root_directory = Path(__file__).resolve().parent
        self.setWindowTitle("Editor de archivos TXT")
        self.resize(800, 600)

        self.file_list = QListWidget()
        self.file_list.currentItemChanged.connect(self.load_selected_file)

        self.text_editor = QTextEdit()
        self.text_editor.setPlaceholderText("Selecciona un archivo para ver su contenido.")

        self.text_editor.setStyleSheet("""
            QTextEdit {
                background-color: #FDF6E3;
                color: #2C3E50;            /* Cambia el color del texto (ej. Azul oscuro/Gris) */
                font-family: 'Consolas';   /* Cambia el tipo de letra (ideal para código/texto) */
                font-size: 16px;          /* Cambia el tamaño de la letra */
            }
        """)

        self.status_label = QLabel()

        self.save_button = QPushButton("Guardar")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_selected_file)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.cancel_selection)

        self.exit_button = QPushButton("Salir")
        self.exit_button.clicked.connect(self.close)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.exit_button)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Archivos .txt en la carpeta del programa:"))
        layout.addWidget(self.file_list)
        layout.addWidget(self.text_editor)
        layout.addWidget(self.status_label)
        layout.addLayout(buttons_layout)

        self.populate_file_list()

    def populate_file_list(self) -> None:
        text_files = sorted(
            (
                path
                for path in self.root_directory.iterdir()
                if path.is_file() and path.name.endswith(".txt")
            ),
            key=lambda path: path.name.casefold(),
        )
        for path in text_files:
            item = QListWidgetItem(path.name)
            item.setData(Qt.UserRole, str(path))
            self.file_list.addItem(item)

    def load_selected_file(
        self, current_item: QListWidgetItem | None, _previous_item: QListWidgetItem | None
    ) -> None:
        if current_item is None:
            self.text_editor.clear()
            self.save_button.setEnabled(False)
            self.status_label.clear()
            return

        selected_path = Path(current_item.data(Qt.UserRole))
        try:
            content = selected_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            self.text_editor.clear()
            self.save_button.setEnabled(False)
            QMessageBox.critical(
                self,
                "Error al leer el archivo",
                f"No se pudo leer {selected_path.name}:\n{error}",
            )
            return

        self.text_editor.setPlainText(content)
        self.save_button.setEnabled(True)
        self.status_label.clear()

    def save_selected_file(self) -> None:
        current_item = self.file_list.currentItem()
        if current_item is None:
            return

        selected_path = Path(current_item.data(Qt.UserRole))
        try:
            selected_path.write_text(self.text_editor.toPlainText(), encoding="utf-8")
        except (OSError, UnicodeError) as error:
            QMessageBox.critical(
                self,
                "Error al guardar el archivo",
                f"No se pudo guardar {selected_path.name}:\n{error}",
            )
            return

        self.status_label.setText(f"Archivo guardado: {selected_path.name}")

    def cancel_selection(self) -> None:
        self.file_list.setCurrentRow(-1)
        self.file_list.clearSelection()
        self.text_editor.clear()
        self.save_button.setEnabled(False)
        self.status_label.clear()


def main() -> None:
    application = QApplication(sys.argv)
    window = TextFileEditor()
    window.show()
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()
