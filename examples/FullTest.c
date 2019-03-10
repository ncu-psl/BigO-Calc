#include <stdio.h>

void hello_world() {
	printf("Hello World!\n");
}

int is_odd(int n) {
	int odd = 0;
	if (n % 2 == 0) {
		odd = 0;
	} else {
		odd = 1;
	}
	return odd;
}

int calc_sum(int n) {
	int i=0,sum = 0;
	for (i = 1; i <= n; i++) {
		sum += i;
	}

	return sum;
}

int calc_odd_sum(int n) {
	int i=0,sum = 0;
	for (i = 1; i <= n; i++) {
	    if(is_odd(i)) {
		    sum = sum + i;
	    }
	}

	return sum;
}

void nested_loop(int n) {
	int i, j;
	int a[100][100];
	for (i = 0; i < n; i++) {
		for (j = 0; j < n; j++) {
			a[i][j] = i * j;
		}
	}
}

int factorial(int n) {
	if (n <= 1)
		return 1;
	return n * factorial(n - 1);
}

int main() {
	int n = 5;
	hello_world();
	is_odd(n);
	calc_sum(n);
	calc_odd_sum(n);
	nested_loop(n);
	factorial(n);
}
