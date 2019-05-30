#include <stdio.h>


void signed_variable_constant(int n) {
    int x=+1;
    int y=-n;
    int m;
    m=1;
    m=n;

    m=+2;
    m=-2;
    m=+n;
    m=-n;
}

void array(int n) {
    int a = 10;
    int one[10];
    int one_init[10] = {1, 2, 3};
    int two[10][10];
    int three[10][10][10];
    int nnn[n][n][n];

    one[0]=1;
    one[1]=n;
}

void cast(int n) {
    long x=n;
    long y=(long)n;
}

void augmented_assignment(int n) {
    n += 1;
    n -= 1;
    n *= 1;
    n /= 1;
    // n <<= 1;
}

void library_function_call() {
    printf("Hello World!\n");
}

void if_else(int n) {
	int odd = 0;

	if (n % 2 == 0) {
		odd = 0;
	} else {
		odd = 1;
	}
}

void if_else_without_block(int n) {
	int odd = 0;

	if (n % 2 == 0)
		odd = 0;
	else
		odd = 1;
}

void if_without_else(int n) {
	int odd = 0;

	// if without else
	if (n % 2 == 0) {
		odd = 0;
	}
}

void if_condition_fc(int n) {
    if(for_loop_n_p(n)) {
    } else {
    }
}

void if_then_fc(int n) {
    if(n==1) {
        for_loop_n_p(n);
    } else {
    }
}

void if_else_fc(int n) {
    if(n==1) {
    } else {
        for_loop_n_p(n);
    }
}

void if_else_cond(int n) {
    if(for_loop_n_p(n)) {
        for_loop_logn_m(n);
    } else {
        for_loop_n_s(n);
    }
}

// O(N), i++
int for_loop_n_p(int n) {
	int i = 0, sum = 0;
	for (i = 1; i <= n; i++) {
		sum += i;
	}

	return sum;
}

// O(N), i--
int for_loop_n_s(int n) {
	int i = 0, sum = 0;
	for (i = n; i >= 1; i--) {
		sum += i;
	}

	return sum;
}

// O(log(N)), i*=2
int for_loop_logn_m(int n) {
	int i = 0, sum = 0;
	for (i = 1; i <= n; i*=2) {
		sum += i;
	}

	return sum;
}

// O(log(N)), i/=2
int for_loop_logn_d(int n) {
	int i = 0, sum = 0;
	for (i = n; i >= 1; i/=2) {
		sum += i;
	}

	return sum;
}

// O(N*N), for * for
void nested_loop(int n) {
	int i, j, a;
	for (i = 0; i < n; i++) {
		for (j = 0; j < n; j++) {
			a = i * j;
		}
	}
}

// recursion
int factorial(int n) {
	if (n <= 1)
		return 1;
	return n * factorial(n - 1);
}

// function call
int main() {
	int n = 5;

    // array
    array(n);

	// library function call
	library_function_call();

	// if else
	if_else(n);
	if_else_without_block(n);
	if_without_else(n);
	if_condition_fc(n);

	// if else with function call
	if_then_fc(n);
	if_else_fc(n);
	if_else_cond(n);

	// Loop O(N), Loop O(log(N))
	for_loop_n_p(n);
	for_loop_n_s(n);
	for_loop_logn_d(n);
	for_loop_logn_m(n);

	// Loop O(N*N)
	nested_loop(n);

	// recursion
	factorial(n);
}
