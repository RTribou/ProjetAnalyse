<center><h2>M2 SSI Project<h2></center>

This script have to aim to generate pictures from analysis of entropy's Linux binary.
For this, you have to launch script 'script.py' in the directory where is your executable you want to analyse. This one will generate a text file.
After, execute  'analyse.py' to generate picture based on text file generated before.

<b>Script.py:</b>
  option: --blocks
     By default, this script calcul entropy section by section. But with this option, it learn binary file bytes per bytes, regardless sections.
     
<b>Analyse.py:</b> no option yet

<b>Main problem:</b>
  -Not enough options
  -Analyse not only binary files(working on it)
  
  
<b>Problems meeting:</b>
  -How to found all sections of a binary file and extract contains?
  -How to generate pictures with good repartition?
