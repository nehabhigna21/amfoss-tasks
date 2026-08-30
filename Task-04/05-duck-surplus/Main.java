import java.io.*;
public class Main{
public static void main(String[] args)throws IOException{
DataInputStream in=new DataInputStream(new BufferedInputStream(System.in,1<<16));
StringBuilder sb=new StringBuilder();
int t=nextInt(in);
while(t-->0){
int n=nextInt(in);
long m=nextInt(in);
for(int i=1;i<n;i++){
int v=nextInt(in);
if(v>m)m=v;
else if(v<m)m+=v;
}
sb.append(m).append('\n');
}
System.out.print(sb);
}
static int nextInt(DataInputStream in)throws IOException{
int r=0,b=in.read();
while(b<'0')b=in.read();
while(b>='0'){
r=r*10+b-'0';
b=in.read();
}
return r;
}
}
