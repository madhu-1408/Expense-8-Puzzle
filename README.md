# Expense-8-Puzzle

## How to Run the Code
1. Extract the `.py` file from the zip folder.
2. Make sure that when running the file in CMD or any terminal, the path is set to the location where the `.py` file is located.
3. You will also need two `.txt` files that define the start state and the goal state. You can name these files however you like, but make sure to include the phrase "End of file" in the 4th line of each text file.
4. With all the necessary files ready, you can call the main function using the following command:

    **expense_8_puzzle.py <start-file> <goal-file> <method> <dump-flag>**

   - If no search method is specified, the default method is A* search.
   - Commands for each search method are as follows:
        - Breadth First Search (BFS): `bfs`
        - Uniform Cost Search (UCS): `ucs`
        - Depth First Search (DFS): `dfs`
        - Iterative Deepening Search (IDS): `ids`
        - Depth Limited Search (DLS): `dls`
        - Greedy Search: `greedy`
        - A* Search: `a*`
   - The dump file flag is set to false by default and will only become true if declared in the command line argument using the "true" command.
   - The dump file will be in the path as the `.py` file.
   - Please ensure that you only pass one name for the start file and one name for the goal file in the command line.
   - Note that the **fringe values of each iteration of the IDS (Iterative Deepening Search) method are printed at the end of the dump file** remaining methods fringes are printed after each iteration.
## Command Line Argument Format
The format of the command line arguments for running the code is as follows:

 expense_8_puzzle.py <start-file> <goal-file> <method> <dump-flag>
