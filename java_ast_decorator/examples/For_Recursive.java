import java.util.*;
class Main {
	public static void forTest(int n) {
		int i, x;
		for (i = 0; i < n; i++) {
			x = i;
		}
	}
	public static int factorial(int n) {
		if (n <= 1)
			return 1;
		return n * factorial(n - 1);
	}
	public static void main (String[] args) {
		Scanner scn;
		int n;
		scn = new Scanner(System.in);
		n = scn.nextInt();
		forTest(n);
		factorial(n);
	}
}
