class Main
{
	public void func1() {
		int i, j, k, w;
		for (i = 1; i < 10; i++) {
			for(j = 1; j < 10; j++) {
				k = i + j;
				w = i * j;
			}
		}
	}

	public void func2(int n) {
		int i;
		for (i = 0; i < n; i++) {
			func1();
		}
	}

	public static void main () {
		Scanner scanner;
		int n;
		scanner = new Scanner(System.in);
		n = scanner.nextInt();
		func2(n);
	}
}
