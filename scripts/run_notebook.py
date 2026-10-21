from pathlib import Path
import nbformat
from nbclient import NotebookClient

root=Path(__file__).resolve().parents[1]
path=root/'spcx_eda_2026_forecast.ipynb'
nb=nbformat.read(path,as_version=4)
NotebookClient(nb,timeout=300,kernel_name='python3',resources={'metadata':{'path':str(root)}},allow_errors=False).execute()
nbformat.write(nb,path)
print('Notebook executed successfully:',path)
