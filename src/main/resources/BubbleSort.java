import java.util.*;
class Main {
	public static void bubbleSort() {
		int[] a = {1,2,5,6,4,3};
		int n;
		n = a.length;
		for(int i = 0; i < n; i++) {
			for(int j = 0; j < n; j++) {
				if(a[i] > a[j]){
					int t;
					t = a[i];
					a[i] = a[j];
					a[j] = t;
				}
			}
		}
	}

	public static void forTest() {
		int i, j;
		for (i = 0; i < 10; i++) {
			j = i + 1;
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
		forTest();
		bubbleSort();
		factorial();
	}
}
