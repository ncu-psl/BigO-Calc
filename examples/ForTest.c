void n_n(int n) {
    int k = 0;
    for(int i=1;i<=n;i++)
        for(int j=1;j<=n;j++)
            k++;
}

void n_logn(int n) {
    int k = 0;
    for(int i=1;i<=n;i++)
        for(int j=1;j<=n;j*=2)
            k++;
}

void n_2_n(int n) {
    int k = 0;
    for(int i=1;i<=n;i++)
        for(int j=1;j<=1<<n;j++)
            k++;
}

void logn_n(int n) {
    int k = 0;
    for(int i=1;i<=n;i*=2)
        for(int j=1;j<=n;j++)
            k++;
}

void logn_logn(int n) {
    int k = 0;
    for(int i=1;i<=n;i*=2)
        for(int j=1;j<=n;j*=2)
            k++;
}

void logn_2_n(int n) {
    int k = 0;
    for(int i=1;i<=n;i*=2)
        for(int j=1;j<=1<<n;j++)
            k++;
}
