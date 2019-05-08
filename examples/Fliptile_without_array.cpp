// 邻接的格子的坐标
const int dx;
const int dy;
// 输入
int M, N;
int tile;
int opt; // 保存最优解
int flip; // 保存中间结果
// 查询(x,y)的颜色
int get(int x, int y) {
	int c = tile;
	for (int d = 0; d < 5; d++) {
		int x2 = x + dx, y2 = y + dy;
		if (0 <= x2 && x2 < M && 0 <= y2 && y2 < N) {
			c += flip;
		}
	}
	return c % 2;
}
// 求出第1行确定情况下的最小操作次数
// 不存在解的话返回-1
int calc() {
// 求出从第2行开始的翻转方法
	for (int i = 1; i < M; i++) {
		for (int j = 0; j < N; j++) {
			if (get(i - 1, j) != 0) {
// (i-1,j)是黑色的话，则必须翻转这个格子
				flip = 1;
			}
		}
	}
// 判断最后一行是否全白
	for (int j = 0; j < N; j++) {
		if (get(M - 1, j) != 0) {
// 无解
			return -1;
		}
	}
// 统计翻转的次数
	int res = 0;
	for (int i = 0; i < M; i++) {
		for (int j = 0; j < N; j++) {
			res += flip;
		}
	}
	return res;
}
void solve() {
	int res = -1;
// 按照字典序尝试第一行的所有可能性
	for (int i = 0; i < 1 << N; i++) {
		memset(flip, 0, sizeof(flip));
		for (int j = 0; j < N; j++) {
			flip = i >> j & 1;
		}
		int num = calc();
		if (num >= 0 && (res < 0 || res > num)) {
			res = num;
			memcpy(opt, flip, sizeof(flip));
		}
	}
	if (res < 0) {
// 无解
		printf("IMPOSSIBLE\n");
	} else {
		for (int i = 0; i < M; i++) {
			for (int j = 0; j < N; j++) {
				printf("%d%c", opt, j + 1 == N ? '\n' : ' ');
			}
		}
	}
}
