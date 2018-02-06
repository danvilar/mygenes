# MyGenes
****
**Overview:** MyGenes is an environment dependant evolution of digital organisms simulator. This script and GUI were developed for my [MSc dissertation](http://danvj.com/modularity.pdf) and shared to assist in new investigations on this topic.

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Text" property="dct:title" rel="dct:type">Mygenes</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="http://www.danvj.com" property="cc:attributionName" rel="cc:attributionURL">Daniel VJ</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.<br />
****

## Quick start

To use My Genes on your operating system you'll need to have **Python 3** installed. Make sure **NumPy** and **SciPy**. If you have no idea how to install these, I suggest downloading the Python 3 distribution by [Anaconda](https://www.continuum.io/downloads).

After the installation, make sure Python is installed correctly on your system by opening the Terminal (or cmd.exe on Windows), type "python" or "python3" and then hit Enter. If it shows something like the image below, it means you're ready to use My Genes.

![TERMINAL](http://i.imgur.com/anoHtqZ.png)

Besides Python and the modules, you'll need to download the repository. 

## Using the GUI

Uncompress the mygenes.zip file you downloaded and double click on **mygenes.py** under the current stable version folder.

## Simulation Parameters

### Populational Parameters

**Individuals Number:** The _fixed_ number of individuals that will figure in each generation.

**Number of Generations:** The number of generation that you want your simulation to run.

### Mutational Parameters
**Node duplication probability (Prob<sub>duplic</sub>):** The probability of a node to be duplicated as a mutational event.

**Node elimination probability (Prob<sub>elim</sub>):** The probability of a node to be eliminated as a mutational event. If the number of nodes in the individual is 1, then Prob<sub>elim</sub> will be equal to zero until it gets more nodes.

**Edge creation/elimination probability (Prob<sub>alpha</sub> and Prob<sub>delta</sub>):** The probability of an edge to appear (Prob<sub>delta</sub>) or disappear (Prob<sub>alpha</sub>) as a mutational event.

### Evaluation Parameters

**Iteration steps:** Fitness is calculated by a boolean analysis. _If you're not sure how to manipulate this parameter use **5**_.

### Additional Parameters

**Replicas:** The number of times you want the simulation to run. You can use the different replicas to perform statistical analysis. _Recomended: 5_.

**Fit selection:** The selection method, _i.e._ which individuals figure in the subsequent generations, you want to use. Currently you have the selection by _fitness **(0)**_ and _random selection **(1)**_.


****
**Feel free to contact me at anytime**
```
Daniel Vilar Jorge
d.vilar-jorge15@imperial.ac.uk
Imperial College London
Department of Surgery and Cancer
```
