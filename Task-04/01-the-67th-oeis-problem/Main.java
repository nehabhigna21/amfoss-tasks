import java.io.*;

// 2218D - The 67th OEIS Problem
// Build a[i] = p[i-1] * p[i] over distinct primes, so gcd(a[i], a[i+1]) = p[i].
// Distinct primes give distinct gcds. Max value ~ 104723^2 < 1e18.

public class Main {
    static final int LIM = 200000;

    public static void main(String[] args) throws IOException {
        int[] p = sieve();

        DataInputStream in = new DataInputStream(new BufferedInputStream(System.in, 1 << 16));
        StringBuilder sb = new StringBuilder();
        int t = nextInt(in);
        while (t-- > 0) {
            int n = nextInt(in);
            if (n == 2) {
                sb.append(p[0]).append(' ').append(p[0]).append('\n');
                continue;
            }
            sb.append(p[0]);
            for (int i = 1; i <= n - 2; i++) {
                sb.append(' ').append((long) p[i - 1] * p[i]);
            }
            sb.append(' ').append(p[n - 2]).append('\n');
        }
        System.out.print(sb);
    }

    static int[] sieve() {
        boolean[] comp = new boolean[LIM + 1];
        int[] p = new int[10005];
        int c = 0;
        for (int i = 2; i <= LIM && c < p.length; i++) {
            if (!comp[i]) {
                p[c++] = i;
                for (long j = (long) i * i; j <= LIM; j += i) comp[(int) j] = true;
            }
        }
        return p;
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
