# TASK-04: The Pirate King's Challenge

Five Codeforces problems, solved in Java. Each one lives in its own folder as a
`Main.java` so it can be pasted straight into the Codeforces submit box.

| # | Problem | Rating | Solution |
|---|---|---|---|
| 1 | [2218D — The 67th OEIS Problem](https://codeforces.com/problemset/problem/2218/D) | 1100 | [`01-the-67th-oeis-problem`](01-the-67th-oeis-problem/Main.java) |
| 2 | [2230B — Digit String](https://codeforces.com/problemset/problem/2230/B) | 1000 | [`02-digit-string`](02-digit-string/Main.java) |
| 3 | [2238A — Another Puzzle from Papyrus](https://codeforces.com/problemset/problem/2238/A) | 800 | [`03-another-puzzle-from-papyrus`](03-another-puzzle-from-papyrus/Main.java) |
| 4 | [2241B — Good times Good times](https://codeforces.com/problemset/problem/2241/B) | 1100 | [`04-good-times-good-times`](04-good-times-good-times/Main.java) |
| 5 | [2237C — Duck Surplus](https://codeforces.com/problemset/problem/2237/C) | 1000 | [`05-duck-surplus`](05-duck-surplus/Main.java) |

Run any of them with:

```bash
cd 02-digit-string
javac Main.java
java Main < input.txt
```

---

## 1. The 67th OEIS Problem

Build a sequence of `n` numbers where every adjacent gcd is different.

The trick is to stop thinking about the numbers and think about the gcds. If I
pick distinct primes `p[1..n-1]` and set `a[i] = p[i-1] * p[i]`, then two
neighbours share exactly one prime, so `gcd(a[i], a[i+1]) = p[i]`. Distinct
primes, distinct gcds, done. The ends are just `p[1]` and `p[n-1]` on their own.

Sum of `n` is `1e4`, so I need at most the 9999th prime, which is `104729`. The
largest value produced is a product of two primes near that, about `1.1e10`,
comfortably under the `1e18` cap. Sieve once at startup, answer every test in
O(n).

## 2. Digit String

A number is divisible by 4 exactly when its last two digits are. Since the
string only holds digits 1–4, that collapses into two rules:

- A single `4` is already a multiple of 4, so every `4` has to go.
- For the rest, `(10*x + y) % 4` is the same as `(2*x + y) % 4`, and checking
  the nine remaining digit pairs, that's 0 only for `(1,2)` and `(3,2)`.

So the only forbidden pattern left is an odd digit sitting somewhere before a
`2`. A string is safe exactly when all its `2`s come before all its odd digits.
That makes it a split-point problem: try every position, keep the `2`s on the
left and the odd digits on the right, and take the best. O(n).

I got this wrong the first time by only deleting the `4`s and stopping there —
the samples caught it immediately, since `3244123` needs 4 deletions and not 2.

## 3. Another Puzzle from Papyrus

Only decrements are allowed, so `a` can never grow, and the cost of all the
decrements is always `sum(a) - sum(b)` no matter what order things are in. That
makes the whole problem a yes/no question about feasibility, with the reorder as
a flat `c` surcharge:

- Don't reorder: works only if `a[i] >= b[i]` at every index.
- Reorder once: sort both arrays and pair them up. Sorted pairing is the most
  forgiving matching there is, so if it fails, nothing works.

Reordering twice is never useful, since one reorder already reaches any
permutation and the decrements don't care about position. Take the cheaper of
the two feasible options, print `-1` if neither is.

## 4. Good times Good times

Given a good `x` (at most two distinct digits), find a good `y` with `x*y` good.

I started by brute-forcing `y` upward and it was ugly — some values of `x` need
to scan tens of thousands of candidates, which is far too slow for `t = 1e4`.

The clean way is to stop searching and build the answer. Let `L` be the number
of digits of `x`, and take `y = 10^L + 1`. Then

```
x * y = x * 10^L + x
```

which is just `x` written down twice in a row. Writing a number twice can't
introduce a new digit, so the product uses exactly the digits of `x` and stays
good. And `y` itself is `1 0...0 1`, only two distinct digits, also good.

Since `x < 1e8` we have `L <= 8`, so `y <= 100000001`, inside the `1e9` limit.
O(1) per test. I checked it against every good `x` below `1e8` — all 20079 of
them pass.

## 5. Duck Surplus

Repeatedly, some `a[i] > a[i+1]` becomes `(a[i+1], a[i] + a[i+1])`, until sorted.
Minimise the largest final pile.

Two observations got me there.

First, always fixing the **leftmost** inversion is optimal. I verified this by
brute-forcing every reachable end state for all small arrays and comparing —
leftmost always ties the best, while "rightmost" is genuinely worse (`[3,2,1]`
gives 6 the leftmost way and 7 the rightmost way).

Second, if you only ever fix the leftmost inversion, the prefix to the left
stays sorted, and each new value `v` just slides left into its place while every
element bigger than `v` picks up `+v` on the way past. So the whole process is
"insert into a sorted list, add `v` to everything above it".

The answer only needs the largest pile, so none of that list has to be stored —
one running maximum `m` is enough:

- `v > m` → `v` is the new biggest, `m = v`
- `v < m` → the max is above `v`, so it gains it: `m += v`
- `v == m` → nothing above `v`, unchanged

That's a single O(n) pass with no data structure at all. The worst case is a
strictly decreasing array of `2e5` values at `1e9`, which tops out near
`2e14` — fits in a `long` with plenty of room.

---

## Testing

Beyond the samples, I checked each solution against a slow-but-obviously-correct
reference:

- **02** — compared to an exhaustive subsequence checker over 1200 random
  strings.
- **03** — compared to a brute force that tries every permutation, 400 cases.
- **05** — compared to a full search over every reachable end state, 1500
  random arrays, plus an exhaustive sweep of all arrays up to length 6 with
  values 1–4.
- **01** and **04** have many valid answers, so instead of comparing output I
  wrote validators: 01 re-computes every adjacent gcd and asserts they're
  distinct and in range; 04 re-checks that `y` and `x*y` are both good.

All five run the maximum-size input well inside the limits.
