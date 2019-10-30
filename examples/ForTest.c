void n_n(int n) {
    int m = m/n;
    for(int i=1;i<m;i++)
        for(int j=1;j<=m;j++)
            k++;
}

void n_logn(int n) {
    int k = n;
    for(int i=1;i<=k+1;i++)
        for(int j=1;j<=k;j*=2)
            k++;
}

void n_2_n(int n) {
    int k = n;
    for(int i=1;i<=k;i++)
        for(int j=1;j<=1<<k;j++)
            k++;
}

void logn_n(int n) {
    int k = n;
    for(int i=1;i<=k;i*=2)
        for(int j=1;j<=k;j++)
            k++;
}

void logn_logn(int n) {
    int k = n;
    for(int i=1;i<=k;i*=2)
        for(int j=1;j<=k;j*=2)
            k++;
}
void logn_2_n(int n) {
    int k = n;
    for(int i=1;i<=k;i*=2)
        for(int j=1;j<=1<<k;j++)
            k++;
}
