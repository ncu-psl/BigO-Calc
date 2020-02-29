import static java.lang.System.out;

/* Class 請勿加上 public 修飾子 */
class Resource implements AutoCloseable{
    public void task() {
        out.println("執行任務");
    }
    
    public void close() throws Exception {
        System.out.println("關閉資源");
    }
}

class AutoCloseableDemo {
    public static void main(String[] args) {
        try(Resource res = new Resource()) {
            res.task();
        } catch(Exception e) {
            e.printStackTrace();
        }
    }
}
