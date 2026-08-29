import java.io.*;
import java.util.*;

// 2238A - Another Puzzle from Papyrus
// Only decrements are allowed, so the total cost of the decrements is always
// sum(a) - sum(b). One reorder is enough (order of a does not affect that sum).
//   - no reorder: possible iff a[i] >= b[i] everywhere, cost sum(a) - sum(b)
//   - one reorder: sort both, possible iff a[i] >= b[i] everywhere, cost c + sum(a) - sum(b)
// Answer is the cheaper feasible option, else -1.

public class Main {
    public static void main(String[] args) throws IOException {
        DataInputStream in = new DataInputStream(new BufferedInputStream(System.in, 1 << 16));
        StringBuilder sb = new StringBuilder();
        int t = nextInt(in);
        while (t-- > 0) {
            int n = nextInt(in), c = nextInt(in);
            int[] a = new int[n], b = new int[n];
            long sum = 0;
            for (int i = 0; i < n; i++) {
                a[i] = nextInt(in);
                sum += a[i];
            }
            for (int i = 0; i < n; i++) {
                b[i] = nextInt(in);
                sum -= b[i];
            }

            boolean plain = true;
            for (int i = 0; i < n; i++) {
                if (a[i] < b[i]) {
                    plain = false;
                    break;
                }
            }

            int[] x = a.clone(), y = b.clone();
            Arrays.sort(x);
            Arrays.sort(y);
            boolean sorted = true;
            for (int i = 0; i < n; i++) {
                if (x[i] < y[i]) {
                    sorted = false;
                    break;
                }
            }

            long ans = -1;
            if (plain) ans = sum;
            if (sorted && (ans == -1 || sum + c < ans)) ans = sum + c;
            sb.append(ans).append('\n');
        }
        System.out.print(sb);
    }

    static int nextInt(DataInputStream in) throws IOException {
        int r = 0, b = in.read();
        while (b < '0') b = in.read();
        while (b >= '0') {
            r = r * 10 + b - '0';
            b = in.read();
        }
        return r;
    }
}
