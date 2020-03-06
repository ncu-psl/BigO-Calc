class Main {
    public static void mian(){
        A a = new A();
        for(int i = 0; i < a.p(); i++){
            i = i;
        }
    }
    
}
class A{
    int p(){
        int k = 0;
        for(int i = 0; i<n; i++){
            k = k+i;
        }
        return k;
    }
}