// 输入
int N;
int M[MAX_N][MAX_N]; // 矩阵
int a[MAX_N]; // a[i]表示第i行最后出现的1的位置——1~n-1
void solve() {
	int res = 0;
	for (int i = 0; i < N; i++) {
		a[i] = -1; // 如果第i行不含1的话，就当作-1
		for (int j = 0; j < N; j++) {
			if (M[i][j] == 1) a[i] = j;
		}
	}
	for (int i = 0; i < N; i++) {
		int pos = -1; // 要移动到第i行的行
		for (int j = i; j < N; j++) {
			if (a[j] <= i) {
				pos = j;
				break;
			}
		}
		// 完成交换
		for (int j = pos; j > i; j--) {
			swap(a[j], a[j - 1]);
			res++;
		}
	}
	printf("%d\n", res);
}
