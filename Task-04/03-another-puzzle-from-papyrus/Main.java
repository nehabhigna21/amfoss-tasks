import java.io.*;
public class Main{
public static void main(String[] args)throws IOException{
BufferedReader br=new BufferedReader(new InputStreamReader(System.in));
int t=Integer.parseInt(br.readLine().trim());
StringBuilder sb=new StringBuilder();
while(t-->0){
String s=br.readLine().trim();
int n=s.length();
int odd=0;
for(int i=0;i<n;i++){
char c=s.charAt(i);
if(c=='1'||c=='3')odd++;
}
int two=0,best=odd;
for(int i=0;i<n;i++){
char c=s.charAt(i);
if(c=='2')two++;
else if(c=='1'||c=='3')odd--;
if(two+odd>best)best=two+odd;
}
sb.append(n-best).append('\n');
}
System.out.print(sb);
}
}
