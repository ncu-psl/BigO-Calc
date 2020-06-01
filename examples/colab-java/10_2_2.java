import java.io.*; 
import static java.lang.System.out;
 
/* Class 請勿加上 public 修飾子 */   
class CheckedExceptionDemo { 
    public static void main(String[] args) { 
        BufferedReader buf = null;
        
        try { 
            buf = new BufferedReader( 
                new InputStreamReader(System.in)); 
                
            out.println("請輸入整數："); 
            int input = Integer.parseInt(buf.readLine()); 
            out.println("input x 10 = " + (input * 10)); 
        } 
        catch(IOException e) { // checked exception
            e.printStackTrace(); 
        } 
        catch(NumberFormatException e) { // runtime exception
            out.println("輸入必須為整數"); 
        } 
        finally {
            try {
                if(buf != null) {
                    buf.close();
                }
            } catch(IOException e) {
                e.printStackTrace();
            }
        }
    } 
}