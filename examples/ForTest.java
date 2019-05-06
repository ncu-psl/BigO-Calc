class Main {
	public static void n_n(int n) {
        int k = 0;
        for(int i=1;i<=n;i++)
            for(int j=1;j<=n;j++)
                k++;
    }

    public static void n_logn(int n) {
        int k = 0;
        for(int i=1;i<=n;i++)
            for(int j=1;j<=n;j*=2)
                k++;
    }

    public static void n_2n(int n) {
        int k = 0;
        for(int i=1;i<=n;i++)
            for(int j=1;j<=1<<n;j++)
                k++;
    }

    public static void logn_n(int n) {
        int k = 0;
        for(int i=1;i<=n;i*=2)
            for(int j=1;j<=n;j++)
                k++;
    }

    public static void logn_logn(int n) {
        int k = 0;
        for(int i=1;i<=n;i*=2)
            for(int j=1;j<=n;j*=2)
                k++;
    }

    public static void logn_2n(int n) {
        int k = 0;
        for(int i=1;i<=n;i*=2)
            for(int j=1;j<=1<<n;j++)
                k++;
    }

}
