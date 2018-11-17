int forTest(int n) {
	int i, x;
	for (i = 0; i < n; i++) {
		x = i;
	}
}

int factorial(int n) {
	if (n <= 1)
		return 1;
	return n * factorial(n - 1);
}

int main() {
	int n;
	scanf("%d", &n);
	forTest(n);
	factorial(n);
	return 0;
}
