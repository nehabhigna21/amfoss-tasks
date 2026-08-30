# TASK-04: The Pirate King's Challenge

Five Codeforces problems, solved in Java. Each one lives in its own folder as a
`Main.java` so it can be pasted straight into the Codeforces submit box.


Run any of them with:


cd 02-digit-string
javac Main.java
java Main < input.txt


---


2. Digit String

A number is divisible by 4 if and only if its last two digits form a number divisible by 4. Since the string contains digits 1 through 4, this simplifies into two rules:

Any single 4 is already divisible by 4, so every 4 must be removed.
For digits (10x+y)%4 equals (2x+y)%4. Checking all nine digit pairs, only (1,2) and (3,2) give a result divisible by 4.

So the only remaining forbidden pattern is a digit appearing before a 2. A valid string must have all 2s come before all digits. This becomes a split-point problem: try every position, keep the 2s on the left and odd digits on the right, and pick the best option. This runs in O(n).

I got this wrong the first time. I only deleted the 4s and stopped there. The sample cases caught it quickly: 3244123 requires four deletions, not two.

3. Another Puzzle from Papyrus

Only decrements are allowed, so a can never grow. The total cost of all decrements is always sum(a)-sum(b), regardless of order. So the whole problem reduces to whether it is feasible with reordering, adding a cost c:

No reordering: works only if a[i]>=b[i] for all indices.
One reordering: sort both. Match them. Sorted pairing is the forgiving matching. If that fails, nothing else works.

Reordering twice is useless because one reordering already reaches any permutation, and decrements do not care about positions. Pick the valid option; if neither works, print -1.

4. Good times Good times

Given a good x with two distinct digits, find a good y such that x*y is also good.

I started by trying values of y upward. It was slow. Some inputs required scanning tens of thousands of candidates, which was way too slow for t=1e4.

The better approach is to build the answer instead of searching. Let L be the number of digits in x and take y=10^L+1. Then:

x*y=x*10^L+x

This is just x written twice in a row. Writing a number twice does not introduce new digits. The product uses only the digits in x, so it stays good. And y itself is 10...01 with two distinct digits, so it is also good.

Since x<1e8, we have L<=8. y<=100000001, well within the 1e9 limit. This gives O(1) per test. I tested it against all x below 1e8. All 20079 of them work.

5. Duck Surplus

Repeatedly, when a[i]>a[i+1], replace it with a[i+1] and a[i]+a[i+1] until the array is sorted. Minimize the final pile.

Two observations led me to the solution.

First, always fixing the leftmost inversion is optimal. I verified this by brute-forcing all end states for small arrays. The leftmost choice always ties for the best, while the rightmost one is worse. For example, [3,2,1] gives 6 with leftmost and 7 with rightmost.

Second, if you only fix the inversion, the prefix stays sorted. Each value v slides left to its place, and every element larger than v gains v as it passes. So the process is insert into a list and add v to everything above.

Since we only care about the pile, we do not need to store the full list. Just track a running maximum m:

If v>m: v is now the biggest, so m=v.
If v<m: the max is above v. It gets +v, so m+=v.
If v==m: nothing is above v, so m stays unchanged.

This is an O(n) pass with no extra data structures.
Worst case: a decreasing array of 2e5 elements, each near 1e9. The result peaks around 2e14. Fits in a long.
