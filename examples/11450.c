#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int dp[ 21 ][ 201 ]; 
int price[ 21 ][ 21 ];
int K[ 21 ];

int main() {
	int N,M,C; 
	while ( scanf("%d",&N) != EOF ) {
		while ( N -- ) {
			scanf("%d%d",&M,&C);
			int i, j,k;
			for (  i = 1 ; i <= C ; ++i ) {
				scanf("%d",&K[i ]);
				for (  j = 1 ; j <= K[ i ] ; ++ j ){
					scanf("%d",&price[ i ][ j ]);
				}
			}

			memset( dp, 0, sizeof( dp ) );
			dp[ 0 ][ 0 ] = 1;

			for (  i = 1 ; i <= C ; ++ i ){
				for (  j = 0 ; j <= M ; ++ j ){
					if ( dp[ i-1 ][ j ] ){
						for (  k = 1 ; k <= K[ i ] ; ++ k ){
							if ( j+price[ i ][ k ] <= M ){
								dp[ i ][ j+price[ i ][ k ] ] = 1;
							}
						}
					}
				}
			}

			int max = 0;
			for (  i = M ; i >= 1 ; -- i ){
				if ( dp[ C ][ i ] ) {
					max = i;break;
				}
			}

			if ( max ) printf("%d\n",max);
			else printf("no solution\n");
		}
		return 0;
	}
}