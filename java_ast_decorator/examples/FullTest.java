import java.util.*;

class FullTest {
	public static void hello_world() {
		System.out.println("Hello World!");
	}

	public static boolean is_odd(int n) {
		boolean odd = false;
		if (n % 2 == 0) {
			odd = false;
		} else {
			odd = true;
		}
		return odd;
	}

	public static int calc_sum(int n) {
		int i = 0, sum = 0;
		for (i = 1; i <= n; i++) {
			sum += i;
		}

		return sum;
	}

	public static int calc_odd_sum(int n) {
		int i = 0, sum = 0;
		for (i = 1; i <= n; i++) {
			if(is_odd(i)) {
				sum = sum + i;
			}
		}

		return sum;
	}

	public static void nested_loop(int n) {
		int i, j;
		int[][] a = new int[100][100];
		for (i = 0; i < n; i++) {
			for (j = 0; j < n; j++) {
				a[i][j] = i * j;
			}
		}
	}

	public static int factorial(int n) {
		if (n <= 1)
			return 1;
		return n * factorial(n - 1);
	}

	public static void main(String[] args) {
		int n = 5;
		hello_world();
		is_odd(n);
		calc_sum(n);
		calc_odd_sum(n);
		nested_loop(n);
		factorial(n);
	}
}
