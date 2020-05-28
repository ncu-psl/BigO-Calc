int fft(int a, int n){
    for (int m = 2; m <= n; m *= 2) {
    int mh = m >> 1;
    for (int i = 0; i < mh; ++i) {
      int w=cos((2*pi)/m*i)-I*sin((2*pi)/m*i);
      for (int j = i; j < n; j += mh) {
        int k = j + mh;
        int x = a[j] - a[k];
        a[j] += a[k];
        a[k] = w * x;
      }
    }
  }
  return a;
}