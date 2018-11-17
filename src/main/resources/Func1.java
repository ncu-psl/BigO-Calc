class Main
{
	public void func1() {
		int i, j, k;
		for (i = 1; i < 10; i++) {
			for(j = 1; j < 10; j++) {
				k = i + j;
			}
		}
	}

	public static void main () {
		int i;
		for (i = 1; i < 3; i++) {
			func1();
		}
	}
}