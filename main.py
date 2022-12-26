from typer import Typer
from os import path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import socketserver
import pdfkit


class FileEvent(FileSystemEventHandler):

	def __init__(self, path, pathout):
		self.path = path
		self.pathout = pathout

	def on_modified(self, event):
		return self.makepdf()

	def makepdf(self) -> bool:
		config = pdfkit.configuration(wkhtmltopdf='wkhtmltox/bin/wkhtmltopdf')
		with open(self.path, 'r') as file:
			pdfkit.from_file(file, self.pathout, configuration=config)
			print('pdf builded')
		return True


app = Typer()


@app.command()
def main(filepath: str, fileout: str):
	if not path.exists(filepath):
		raise 'No existe el archivo dado: ' + filepath

	observer = Observer()
	fe = FileEvent(filepath, fileout)
	fe.makepdf()
	observer.schedule(
		fe,
		filepath,
		recursive=False
	)
	observer.start()
	try:
		while observer.is_alive():
			observer.join(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()


if __name__ == '__main__':
	app()
