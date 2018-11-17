import java.util.*;
class Main {
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
		factorial(n);
	}
}
