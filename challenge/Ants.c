// 输入
int L, n;
int x[MAX_N];
void solve() {
// 计算最短时间
	int minT = 0;
	for (int i = 0; i < n; i++) {
		minT = max(minT, min(x[i], L - x[i]));
	}
// 计算最长时间
	int maxT = 0;
	for (int i = 0; i < n; i++) {
		maxT = max(maxT, max(x[i], L - x[i]));
	}
	printf("%d %d\n", minT, maxT);
}
