import argparse
import glob
import pandas as pd
import matplotlib.pyplot as plt
import sys

def ChangeFileExt(InFile, OldFileExt, NewFileExt):
    '''
    This function will replace a one file extension with another
    Param:
        InFile - str, Filename to be changed
        OldFileExt - str, extension to be changed
        NewFileExt - str, new extension
    Returns:
        NewFileName - str, File with new extension
    '''
    try:
        OldExtLenSplit = len(InFile.split(OldFileExt)[1])
    except:
        error_text_01 = f'File extensions must be at the end of the InFile string\n{InFile}\n{OldFileExt}'
        sys.exit(error_text_01)
    if (OldFileExt[0] == "." and NewFileExt[0] == "." and OldExtLenSplit == 0):
        NewFileName = InFile.split(OldFileExt)[0] + NewFileExt
        return NewFileName
    else:
        error_text_02 = f'File extensions should start with a "." and OldFileExt must be at the end of \
            the InFile string\n{InFile}\n{OldFileExt}\n{NewFileExt}'
        sys.exit(error_text_02)

def Create_Graph_CLC(Stats_File, Outfile):
    """
    This function uses the pandas and matlab library and is designed to generate a coverage 
    graph, utilizing a previously produced tab-separated statistics text file 
    created by CLC Genomics Workbench. This file comprises the 
    headers: Mapping, Reference position, Name, Region, Target region position, Reference base,
    and Coverage.
    Params:
        Stats_File - str, tab separated text file
    Returns:
        CoverageGraph - str, graph file (.png) demonstrating read coverage across reference genome
    """
    plt.close("all")
    StatDataFrame = pd.read_csv(Stats_File, sep=',', quoting=3)
    # Graph Coverage and Save PNG
    CoverageGraph = StatDataFrame.plot(kind = 'line',
        x = 'Reference position',
        y = 'Coverage',
        logy = True,
        legend = False,
        title = 'Read Coverage',
        ylabel = 'Depth of Coverage',
        figsize= (20, 10),
        color= COLOR
    )
    CoverageFigure = CoverageGraph.get_figure()
    CoverageFigure.savefig(Outfile)
    plt.close("all")
    return Outfile

## Arguments
DESCRIPTION_START = 'Creating Coverage Graph From CLC Stats'
DESCRIPTION_END = 'Example:  python Create_Coverage_Graphs_From_CLC_CSV.py --directory "PATH/TO/CLC/FILES/" --color darkblue'
parser = argparse.ArgumentParser(description=DESCRIPTION_START, epilog=DESCRIPTION_END)
parser.add_argument('--directory', action="store", dest='directory', help="Path to the .csv CLC Stat files", required=True)
parser.add_argument('--color', action="store", dest='linecolor', help="Color of the line", required=False, default = 'darkblue')

args = parser.parse_args()
DIRECTORY = args.directory
COLOR = args.linecolor

## Format Directory String and Collect Files
directory_fmt = DIRECTORY.replace("\\", "/")
directory_fmt = directory_fmt + "/" if directory_fmt[-1] != "/" else directory_fmt
CLC_files = glob.glob(directory_fmt + "*.csv")

## Main Loop
print('~~~~Starting Conversions~~~~')
for file in CLC_files:
    print(f'Creating a graph from {file}')
    GraphFIle = ChangeFileExt(InFile = file, OldFileExt = ".csv", NewFileExt= ".png")
    Create_Graph_CLC(Stats_File = file, Outfile= GraphFIle)
print('~~~~Complete!~~~~')