public class Main {
	static int loop1(int n) {
		int s = 0;
		for (int i = 1; i < n + 1; i++) {
			for (int j = 1; j < i * i + 1; j++) {
				s = s + 1;
			}
		}
		return s;
	}

	static int loop2(int n) {
		int s = 0;
		for (int i = 1; i < n + 1; i++) {
			for (int j = 1; j < i + 1; j++) {
				s = s + 1;
			}
		}
		return s;
	}

	static void loop3(int n) {
		int j = n;
		for (int i = 0; i <= j; i++) {
			j = j - 1;
		}
	}

	static void loop4a(int n) {
		int j = n;
		for (int i = n; i > 0; i = (i - 1) / 2) {
		}
	}

	static int loop5(int n) {
		int s = 1;
		for (int i = 1; i <= n; i *= 2) {
			for (int j = 1; j < i + 1; j++) {
				s = s + 1;
			}
		}
		return s;
	}

	static int loop6(int n) {
		int s = 1;
		// for (int i = 1; i * i <= n; i = i + i) {
		// 	s = s + 1;
		// }
		return s;
	}

	static int _loop1(int n) {
		int s = 0;
		for (int i = 1; i < n + 1; i++) {
			for (int j = 1; j < n + 1; j++) {
				s = s + 1;
			}
		}
		return s;
	}

	static void _loop2(int n) {
		for (int i = 0; i < n; i++) {
			for (int j = i; j > 0; j /= 2) {
			}
		}
	}


	static void nlogn(int n) {
		for (int i = 0; i < n; i++) {
			for (int j = 1; j < n; j += j) {
			}
		}
	}

	static void logn(int n) {
		for (int j = 1; j < n; j += j) {
		}
	}

	static int logsq(int n) {
		int s = 0;
		for (int i = 1; i <= n; i = 2 * i) {
			for (int j = 1; j < i; j = 2 * j) {
				s = s + 1;
			}
		}
		return s;
	}

	static int arith(int n) {
		int s = 0;
		for (int i = 37 * n; i < 53 * n; i++) {
			s = s + 1;
		}
		return s;
	}
}
