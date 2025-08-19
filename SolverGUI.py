
import LizardSudokuSolver as s
import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QFrame,
    QTextEdit,
    QDialog,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import (
    QIntValidator,
    QPainter,
    QColor,
    QPen,
    QFont,
    QMouseEvent,
    QKeyEvent,
)
from PySide6.QtCore import Qt, Signal, Slot


class SudokuCell(QFrame):

    clicked = Signal(int, int)

    def __init__(self, row, col, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)
        self.setFixedSize(50, 50)

        self.main_label = QLabel(self)
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.main_label.font()
        font.setPointSize(16)
        self.main_label.setFont(font)

        self.notes_label = QLabel(self)
        self.notes_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.notes_label.setWordWrap(True)
        font = self.notes_label.font()
        font.setPointSize(8)
        self.notes_label.setFont(font)

        self.main_label.setGeometry(0, 0, 50, 50)
        self.notes_label.setGeometry(2, 0, 46, 48) # Inset for padding

        self.value = 0
        self.notes = set()
        self.is_selected = False
        self.notes_mode = False

    def paintEvent(self, event):

        super().paintEvent(event)
        painter = QPainter(self)
        if self.is_selected:
            painter.setPen(Qt.PenStyle.NoPen)
            if self.notes_mode:

                painter.setBrush(QColor(144, 238, 144, 255))
                painter.drawRect(0, 0, 15, 15)
            else:
                painter.setBrush(QColor(144, 238, 144, 128))
                painter.drawRect(self.rect().adjusted(0, 0, -1, -1))

    def set_value(self, value):
        self.clear_notes()
        self.value = value
        if value == 0:
            self.main_label.setText("")
        else:
            self.main_label.setText(str(value))
        self.update()

    def clear_notes(self):
        self.notes.clear()
        self.notes_label.setText("")
        self.update()

    def set_notes(self, notes_list):
        self.notes = set(notes_list)
        self.notes_label.setText(" ".join(map(str, sorted(list(self.notes)))))

    def toggle_note(self, note):
        if note in self.notes:
            self.notes.remove(note)
        else:
            self.notes.add(note)
        self.notes_label.setText(" ".join(map(str, sorted(list(self.notes)))))
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.notes_mode = False
        elif event.button() == Qt.MouseButton.RightButton:
            self.notes_mode = True
        self.clicked.emit(self.row, self.col)
        self.update()

    def set_selected(self, selected):
        self.is_selected = selected
        self.update()


class SudokuGrid(QWidget):

    def __init__(self, size, parent=None):
        super().__init__(parent)
        self.size = size
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid_layout)

        self.cells = []
        for r in range(size * size):
            row = []
            for c in range(size * size):
                cell = SudokuCell(r, c)
                cell.clicked.connect(self.cell_clicked)
                self.grid_layout.addWidget(cell, r, c)
                row.append(cell)
            self.cells.append(row)

        self.selected_cell = None
        self.data = [[0] * (size * size) for _ in range(size * size)]

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor("black"))

        width = self.cells[0][0].width()
        height = self.cells[0][0].height()
        
        for i in range(self.size * self.size + 1):
            pen.setWidth(4 if i % self.size == 0 else 1)
            painter.setPen(pen)
            
            painter.drawLine(i * width, 0, i * width, self.size * self.size * height)
            painter.drawLine(0, i * height, self.size * self.size * width, i * height)

    @Slot(int, int)
    def cell_clicked(self, row, col):
        if self.selected_cell:
            self.selected_cell.set_selected(False)
        self.selected_cell = self.cells[row][col]
        self.selected_cell.set_selected(True)
        self.setFocus()

    def keyPressEvent(self, event: QKeyEvent):
        if not self.selected_cell:
            return

        if event.key() >= Qt.Key.Key_1 and event.key() <= Qt.Key.Key_9:
            number = int(event.text())
            if self.selected_cell.notes_mode:
                self.selected_cell.toggle_note(number)
            else:
                self.selected_cell.set_value(number)
                self.data[self.selected_cell.row][self.selected_cell.col] = number
        
        elif event.key() in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
            if self.selected_cell.notes_mode:
                self.selected_cell.clear_notes()
            else:
                self.selected_cell.set_value(0)
                self.data[self.selected_cell.row][self.selected_cell.col] = 0


class SolutionLogWindow(QDialog):

    def __init__(self, log_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Solution Log")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        log_display = QTextEdit()
        log_display.setReadOnly(True)
        log_display.setText(log_text)
        log_display.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                color: #333;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(log_display)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver GUI")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        top_controls_layout = QHBoxLayout()
        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText("Enter grid size (e.g., 3 for 9x9)")
        self.size_input.setValidator(QIntValidator(2, 5, self))
        self.generate_button = QPushButton("Generate Grid")
        self.generate_button.clicked.connect(self.generate_grid)
        self.solve_button = QPushButton("Solve")
        self.solve_button.clicked.connect(self.solve_puzzle)
        self.log_button = QPushButton("Show Log")
        self.log_button.clicked.connect(self.show_log)
        self.load_button = QPushButton("Load Grid")
        self.load_button.clicked.connect(self.load_grid)
        self.save_button = QPushButton("Save Grid")
        self.save_button.clicked.connect(self.save_grid)
        self.save_button.setEnabled(False)

        top_controls_layout.addWidget(QLabel("Grid Size:"))
        top_controls_layout.addWidget(self.size_input)
        top_controls_layout.addWidget(self.generate_button)
        top_controls_layout.addStretch()
        top_controls_layout.addWidget(self.solve_button)
        top_controls_layout.addWidget(self.log_button)
        top_controls_layout.addWidget(self.load_button)
        top_controls_layout.addWidget(self.save_button)
        self.main_layout.addLayout(top_controls_layout)

        self.sudoku_grid_container = QWidget()
        self.grid_layout_container = QVBoxLayout(self.sudoku_grid_container)
        self.main_layout.addWidget(self.sudoku_grid_container)

        self.sudoku_grid = None
        self.solution_log = "Solver has not been run yet."
        
        self.setStyleSheet("""
            QMainWindow { background-color: #e8e8e8; }
            QPushButton {
                background-color: #4CAF50; color: white; padding: 8px;
                border-radius: 4px; font-size: 14px;
            }
            QPushButton:hover { background-color: #45a049; }
            QLineEdit {
                padding: 5px; border: 1px solid #ccc;
                border-radius: 4px; font-size: 14px;
            }
            QLabel { font-size: 14px; }
        """)

    def generate_grid(self):
        if self.sudoku_grid:
            self.grid_layout_container.removeWidget(self.sudoku_grid)
            self.sudoku_grid.deleteLater()
        
        try:
            size = int(self.size_input.text())
            if size < 2: return
        except ValueError:
            return

        self.sudoku_grid = SudokuGrid(size=size)
        self.grid_layout_container.addWidget(self.sudoku_grid, alignment=Qt.AlignmentFlag.AlignCenter)
        self.save_button.setEnabled(True)


    def save_grid(self):
        if not self.sudoku_grid: return

        path, _ = QFileDialog.getSaveFileName(self, "Save Grid", "", "JSON Files (*.json)")
        if not path: return

        grid_data = []
        for r in range(self.sudoku_grid.size * self.sudoku_grid.size):
            row_data = []
            for c in range(self.sudoku_grid.size * self.sudoku_grid.size):
                cell = self.sudoku_grid.cells[r][c]
                row_data.append({"value": cell.value, "notes": list(cell.notes)})
            grid_data.append(row_data)

        save_data = {"size": self.sudoku_grid.size, "grid": grid_data}
        try:
            with open(path, 'w') as f:
                json.dump(save_data, f, indent=4)
        except IOError as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {e}")

    def load_grid(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Grid", "", "JSON Files (*.json)")
        if not path: return

        try:
            with open(path, 'r') as f:
                data = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            QMessageBox.critical(self, "Error", f"Could not load or parse file: {e}")
            return
        
        loaded_size = data.get("size")
        self.size_input.setText(str(loaded_size))
        self.generate_grid()

        loaded_grid_data = data.get("grid", [])
        for r, row_data in enumerate(loaded_grid_data):
            for c, cell_data in enumerate(row_data):
                value = cell_data.get("value", 0)
                notes = cell_data.get("notes", [])
                
                self.sudoku_grid.data[r][c] = value
                cell_widget = self.sudoku_grid.cells[r][c]
                
                if value != 0:
                    cell_widget.set_value(value)
                else: # Set value to 0 and then add notes
                    cell_widget.set_value(0)
                    cell_widget.set_notes(notes)

    def solve_puzzle(self):
        if not self.sudoku_grid:
            return
            
        puzzle_data = self.sudoku_grid.data

        grid = s.CreateSudokuGrid(self.sudoku_grid.size)


        for i in range(len(puzzle_data)):
            for j in range(len(puzzle_data)):
                if puzzle_data[i][j] != 0:
                    grid = s.PlaceNumber(grid, puzzle_data[i][j], i, j)

        solution_steps = grid["solution_log"]

        for i in range(len(puzzle_data)):
            for j in range(len(puzzle_data)):
                self.sudoku_grid.cells[i][j].set_value(grid["solution"][i][j])

        self.solution_log = "\n".join(solution_steps)
        print("Solver finished.")

    def show_log(self):
        log_window = SolutionLogWindow(self.solution_log, self)
        log_window.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())