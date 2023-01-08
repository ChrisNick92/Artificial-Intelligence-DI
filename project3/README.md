In this README document we explain how to use and run the `kenken.py` in order to solve the [Kenken Puzzle](http://www.kenkenpuzzle.com). The format for the kenken puzzle is illustrated by the following example:

Suppose that the puzzle is the following:


<img src="grid6_6.png" alt="drawing" width="600"/>

Then, the format for the input is the following:

```
6
11#0-6#+
2#1-2#/
3#7-8#-
20#3-9#*
6#4-5-11-17#*
3#10-16#/
240#12-13-18-19#*
6#14-15#*
6#20-26#*
7#21-27-28#+
30#22-23#*
6#24-25#*
9#29-35#+
8#30-31-32#+
2#33-34#/
```

The number in the first row specifies the size of the kenken puzzle. In the above example a puzzle of 6x6 is given. In the second row, the first number appearing before the first # indicates the value of the clique. The numbers placed between the # and separated by hyphens (-) indicate the cells contained in the clique and the operator at the end of the line specifies the operation between the numbers in the clique. For example, the row `11#0-6#+` means that the cells `0,6` must add up to 11. Cell numbering start with cell `0` placed on the top-left corner of the grid and by reading each line sequentially, end with cell `N-1` located at the bottom-right corner of the grid with size $N\times N$.

The script `kenken.py` is designed in such a way that the user may select its own input puzzle as well as the algorithm to solve it. The flag `-i` specifies the `.txt` file of the puzzle in the aforementioned format. For example, an execution

```bash
python kenken.py -i example.txt
```

solves the puzzle described in `example.txt` with the backtracking algorithm without any heuristics. The user may use the optional argument `--unasigned_variable` to select the Minimum Remaining Value (MRV) heuristc for the selection order of the variables. For example, executing

```bash
python kenken.py -i example.txt --unassigned_variable mrv
```

solve the puzzle described in `example.txt` by using mrv as a variable selection. The default value of `--unassigned_variable` is `first_unassigned_variable` which corresponds to the selection of first variable that hasn't been selected.

Two heuristics can be used for inference: Forward checking (FC) and Maintaining Arc Conistency (MAC). The flag `--inference` handles this option. The choiches are `fc, mac, no_inference`. For example, the command

```bash
python kenken.py -i example.txt --unassigned_variable mrv --inference fc
```

solves the puzzle by using backtracking with mrv and forward checking.

The command `python kenken.py` solves all puzzles located in `inputs` directory. The answers to this puzzles are given in `solutions` directory.