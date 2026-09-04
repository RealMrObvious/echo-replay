from PyQt6.QtWidgets import QApplication, QFileDialog
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import QEvent, QObject, pyqtSignal, pyqtSlot, QPropertyAnimation, QEasingCurve, QMimeData, QUrl, Qt

class ShareTab(QObject):
    file_selected  = pyqtSignal(str)

    def __init__(self, ui):
            super().__init__()
            self.ui = ui
            self.most_recent_compressed_file_path = None
            self.pick_files_enabled = True

            self.set_ui_to_start()
    
            self.ui.share_copy_button.clicked.connect(self.copy_file_to_clipboard)
            self.ui.share_quit_button.clicked.connect(self.set_ui_to_start)

            self.progress_animation = QPropertyAnimation(
                self.ui.share_progress_bar,
                b"value"
            )
            self.progress_animation.setDuration(300)
            self.progress_animation.setEasingCurve(
                QEasingCurve.Type.OutCubic
            )

    def eventFilter(self, obj, event):
        if obj is self.ui.drop_frame and self.pick_files_enabled:
            return self.handle_files(event)

        return super().eventFilter(obj, event)

    def handle_files(self, event):
        if event.type() == QEvent.Type.DragEnter:
            if event.mimeData().hasUrls():
                event.acceptProposedAction()
                return True

        elif event.type() == QEvent.Type.Drop:
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    print("Dropped:", file_path)
                    self.start_encoding_process(file_path)
                    
                    break

            event.acceptProposedAction()
            return True

        elif event.type() == QEvent.Type.MouseButtonPress:
            file_path, _ = QFileDialog.getOpenFileName(
                self.ui.share_tab,
                "Select Video",
                "",
                "Video Files (*.mp4 *.mkv *.avi *.mov *.webm);;All Files (*)"
            )

            if file_path:
                print("Selected:", file_path)
                self.start_encoding_process(file_path)
                return True

        return False

    def set_ui_to_start(self):
        self.ui.drop_frame.installEventFilter(self)
        self.ui.share_progress_bar.setValue(0)
        self.ui.share_progress_bar.hide()
        self.ui.share_copy_button.hide()
        self.ui.share_quit_button.hide()
        self.ui.share_file_thumbnail.hide()
        self.ui.share_file_thumbnail.setPixmap(QPixmap())
        self.ui.drop_frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.ui.share_file_label.setStyleSheet("")
        self.ui.share_file_label.setText("Drag files here or click to browse")

        self.pick_files_enabled = True

    def start_encoding_process(self, file_path):
        self.ui.share_file_label.setText(f"Compressing {file_path}")
        self.ui.share_progress_bar.show()
        self.ui.share_file_thumbnail.show()
        self.pick_files_enabled = False
        self.ui.drop_frame.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        self.file_selected.emit(file_path)

    def copy_file_to_clipboard(self):
        if self.most_recent_compressed_file_path:
            mime_data = QMimeData()

            mime_data.setUrls([
                QUrl.fromLocalFile(str(self.most_recent_compressed_file_path))
            ])

            QApplication.clipboard().setMimeData(mime_data)

    @pyqtSlot(int)
    def update_progress(self, progress):
        print(f"Encoding progress: {progress}")
        self.progress_animation.stop()
        self.progress_animation.setStartValue(
            self.ui.share_progress_bar.value()
        )
        self.progress_animation.setEndValue(progress)
        self.progress_animation.start()

    @pyqtSlot(bool, str)
    def encoding_finished(self, success, compressed_file_path):
        print(f'Encoding finished {"successful" if success else "with issues"}. Path: {compressed_file_path}')
        self.ui.share_progress_bar.hide()
        self.ui.share_copy_button.show()
        self.ui.share_file_label.setText("Done compressing")
        self.ui.share_quit_button.show()
        self.most_recent_compressed_file_path = compressed_file_path

    @pyqtSlot(bool, str)
    def encoding_error(self, error_occured, error_msg):
        if error_occured: print(f"An encoding error has occured: {error_msg}")
        self.ui.share_file_label.setText(f"An encoding error has occured: {error_msg}")
        self.ui.share_file_label.setStyleSheet("color: red;")
        self.ui.share_progress_bar.hide()
        self.ui.share_quit_button.show()

    @pyqtSlot(str)
    def set_thumbnail(self, thumbnail_path):
        print(f"Recieved thumbnail: {thumbnail_path}")
        if(thumbnail_path):
            self.ui.share_file_thumbnail.setPixmap(QPixmap(thumbnail_path))
