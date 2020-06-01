import java.util.Scanner;

/* Class 請勿加上 public 修飾子 */
class UserLogin {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("使用者名稱：");
        String username = scanner.next();

        System.out.print("使用者密碼：");
        String password = scanner.next();

        if("caterpillar".equals(username) 
                    && "1975".equals(password)) {

            System.out.println("秘密資訊在此！");
        }
        else {
            System.out.println(username + 
                    " 你好，輸入的登入資料有誤，請重新輸入！");
        }
        
    }
}