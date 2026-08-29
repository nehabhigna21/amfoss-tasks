import java.io.*;

// 2241B - Good times Good times
// Take y = 10^L + 1, where L is the number of digits of x. Then
// x * y = x * 10^L + x, which is just x written twice in a row, so it uses
// exactly the digits of x and stays good. y itself is 1 0...0 1, also good.
// x < 1e8 gives L <= 8, so y <= 100000001 <= 1e9.

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int t = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        while (t-- > 0) {
            String x = br.readLine().trim();
            long y = 1;
            for (int i = 0; i < x.length(); i++) y *= 10;
            sb.append(y + 1).append('\n');
        }
        System.out.print(sb);
    }
}
