// 输入
int n, a[MAX_N];
void solve() {
	int ans = 0; // 答案
	// 让i < j < k，这样棍子就不会被重复选中了
	for (int i = 0; i < n; i++) {
		for (int j = i + 1; j < n; j++) {
			for (int k = j + 1; k < n; k++) {
				int len = a[i] + a[j] + a[k]; // 周长
				int ma = max(a[i], max(a[j], a[k])); // 最长棍子的长度
				int rest = len - ma; // 其余两根棍子的长度之和
				if (ma < rest) {
				// 可以组成三角形，如果可以更新答案则更新
					ans = max(ans, len);
				}
			}
		}
	}
	// 输出
	printf("%d\n", ans);
}
