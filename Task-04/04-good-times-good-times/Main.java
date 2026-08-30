import java.io.*;
public class Main{
public static void main(String[] args)throws IOException{
BufferedReader br=new BufferedReader(new InputStreamReader(System.in));
int t=Integer.parseInt(br.readLine().trim());
StringBuilder sb=new StringBuilder();
while(t-->0){
String x=br.readLine().trim();
long y=1;
for(int i=0;i<x.length();i++)y*=10;
sb.append(y+1).append('\n');
}
System.out.print(sb);
}
}
