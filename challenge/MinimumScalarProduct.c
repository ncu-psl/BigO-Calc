typedef long long ll;
// 输入
int n;
int v1[MAX_N], v2[MAX_N];
void solve() {
	sort(v1, v1 + n);
	sort(v2, v2 + n);
	ll ans = 0;
	for (int i = 0; i < n; i++) ans += (ll)v1[i] * v2[n - i - 1];
	printf("%lld\n", ans);
}
