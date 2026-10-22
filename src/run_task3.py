"""Collect then execute every notebook cell in a fresh Python process."""
import argparse, os
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from collect_task3 import collect
from process_data import ROOT

def execute_in_process(notebook):
    # For restricted hosts where Jupyter cannot open local sockets.
    from IPython.core.interactiveshell import InteractiveShell
    from IPython.utils.capture import capture_output
    shell=InteractiveShell.instance()
    count=0
    for cell in notebook.cells:
        if cell.cell_type!="code": continue
        count+=1
        with capture_output() as captured:
            result=shell.run_cell(cell.source,store_history=True)
        if result.error_before_exec: raise result.error_before_exec
        if result.error_in_exec: raise result.error_in_exec
        outputs=[]
        if captured.stdout: outputs.append(nbformat.v4.new_output("stream",name="stdout",text=captured.stdout))
        if captured.stderr: outputs.append(nbformat.v4.new_output("stream",name="stderr",text=captured.stderr))
        for output in captured.outputs:
            outputs.append(nbformat.v4.new_output("display_data",data=output.data,metadata=output.metadata))
        cell.outputs=outputs;cell.execution_count=count
    notebook.metadata["execution_method"]="Fresh-process sequential IPython execution; local Jupyter sockets unavailable on build host. Re-run with standard Jupyter kernel on Windows."

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--config",type=Path,default=ROOT/"configs/task3_smoke.json")
    p.add_argument("--analysis-only",action="store_true")
    p.add_argument("--in-process",action="store_true",help="Use sequential IPython without kernel sockets")
    args=p.parse_args()
    if not args.analysis_only: collect(args.config)
    path=ROOT/"notebooks/01_data_analysis.ipynb"
    notebook=nbformat.read(path,as_version=4)
    for cell in notebook.cells:
        if cell.cell_type=="code": cell.outputs=[];cell.execution_count=None
    if args.in_process:
        os.chdir(ROOT/"notebooks")
        execute_in_process(notebook)
    else:
        client=NotebookClient(notebook,kernel_name="python3",timeout=300,resources={"metadata":{"path":str(ROOT/"notebooks")}})
        client.execute(cwd=str(ROOT/"notebooks"))
        notebook.metadata["execution_method"]="Restarted Jupyter kernel; sequential execution via nbclient"
    nbformat.write(notebook,path)
    print("Task 3 analysis completed. Executed notebook saved.")
