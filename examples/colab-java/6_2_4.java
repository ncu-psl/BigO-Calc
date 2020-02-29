import java.io.*;
 
/* Class 請勿加上 public 修飾子 */
class UseRegularExpression { 
    public static void main(String args[]) throws IOException { 
        BufferedReader reader = 
            new BufferedReader(
                new InputStreamReader(System.in));

        System.out.println(
            "abcdefgabcabc".replaceAll(".bc", "###")); 

        String phoneRegx = "[0-9]{4}-[0-9]{6}";
        String urlRegx = "<a.+href*=*['\"]?.*?['\"]?.*?>";
        String emailRegx = "^[_a-z0-9-]+(.[_a-z0-9-]+)*" + 
                            "@[a-z0-9-]+([.][a-z0-9-]+)*$";

        System.out.print("輸入手機號碼: "); 
        String input = reader.readLine();

        if(input.matches(phoneRegx)) {
            System.out.println("格式正確"); 
        }
        else { 
            System.out.println("格式錯誤");
        }

        System.out.print("輸入 href 標籤: "); 
        input = reader.readLine();

        // 驗證href標籤 
        if(input.matches(urlRegx)) {
            System.out.println("格式正確"); 
        }
        else {
            System.out.println("格式錯誤");
        }

        System.out.print("輸入電子郵件: "); 
        input = reader.readLine();

        // 驗證電子郵件格式 
        if(input.matches(emailRegx)) {
            System.out.println("格式正確"); 
        }
        else {
            System.out.println("格式錯誤"); 
        }
    } 
}