# SokobanGame
Sokoban Game by Michal Zimering and Noam Sabban for Formal Verification Course Project

## How to run the game
Input XSB board should be placed in the Input folder as .txt files.

Run the following command in the terminal:

For Part 2: 
```python sokoban.py example.txt ``` with the desired example file

For Part 3:
```
python sokoban.py example.txt BDD 
python sokoban.py example.txt SAT
``` 

with the desired example file and the desired solver engine (BDD or SAT)

#### In part 2 and 3 running this command will create an SMV file in SMV_files folder named after the example selected.
#### it will also run it with nuXmv depending on the solver selected and create an output file (.out) in the Output folder, named as the example selected.
#### Resolvability, LURD Solutions and running time of each game run can be found at the very end of each output file.


For Part 4:

```
./nuXmv -int example2.txt  
go_bmc
check_ltlspec_bmc -P first
check_ltlspec-bmc -P second
check_ltlspec-bmc -P ...
check_ltlspec-bmc -P ...
```
with the desired example file, and ```check_ltlspec_bmc - P``` for each iteration 

