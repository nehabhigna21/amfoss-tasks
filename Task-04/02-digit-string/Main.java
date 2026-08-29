import java.io.*;

// 2230B - Digit String
// A number is divisible by 4 iff its last two digits are. Digits are 1..4, so:
//   - every '4' is a 1-digit multiple of 4 and must go;
//   - for the rest, (10*x + y) % 4 == (2*x + y) % 4 is 0 only for (1,2) and (3,2),
//     i.e. an odd digit followed later by a '2'.
// So keep a block of 2s, then a block of odd digits. Try every split point.

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int t = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        while (t-- > 0) {
            String s = br.readLine().trim();
            int n = s.length();
            int odd = 0;
            for (int i = 0; i < n; i++) {
                char c = s.charAt(i);
                if (c == '1' || c == '3') odd++;
            }
            // best = most characters we can keep: 2s from the prefix, odd digits from the suffix
            int two = 0, best = odd;
            for (int i = 0; i < n; i++) {
                char c = s.charAt(i);
                if (c == '2') two++;
                else if (c == '1' || c == '3') odd--;
                if (two + odd > best) best = two + odd;
            }
            sb.append(n - best).append('\n');
        }
        System.out.print(sb);
    }
}
