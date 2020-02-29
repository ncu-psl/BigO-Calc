/* Class 請勿加上 public 修飾子 */
class CharAtString { 
    public static void main(String[] args) { 
        String text = "One's left brain has nothing right.\n" + 
                        "One's right brain has nothing left.\n"; 
    
        System.out.println("字串內容: "); 
        for(int i = 0; i < text.length(); i++) {
            System.out.print(text.charAt(i)); 
        }

        System.out.println("\n第一個 left: " + 
                                text.indexOf("left")); 
        System.out.println("最後一個 left: " + 
                                text.lastIndexOf("left")); 

        System.out.println("\n字元 Array 內容: "); 
        for(char c : text.toCharArray()) {
            System.out.print(c); 
        }
    } 
} 