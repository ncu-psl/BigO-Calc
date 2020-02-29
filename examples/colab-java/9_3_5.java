import static java.lang.System.out;

/* Class 請勿加上 public 修飾子 */
class ExceptionDemo { 
    public static void main(String[] args) { 
        try { 
            throw new ArithmeticException("例外測試"); 
        } 
        catch(Exception e) { 
            out.println(e); 
        } 
    } 
} 