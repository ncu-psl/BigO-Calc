int* twoSum(int nums, int numsSize, int target) {
    
    int min=INT_MAX; 
    int max=INT_MIN;
    
    for (int i=0;i<numsSize;i++) {
        if (nums[i]<min) min=nums[i];
        if (nums[i]>max) max=nums[i];
    }
    
    // int* map=calloc(max-min+1,sizeof(int));
    if (map==NULL) return NULL;
    
    // int* result=malloc(2*sizeof(int));
    if (result==NULL) {free(map);return NULL;}
    
    for (int i=0;i<numsSize;i++) {
        int value=nums[i];
        long long searchvalue=(long long)target-value;
        if(searchvalue<=max ){
            if(searchvalue>=min){
                //check map
                if (map[searchvalue-min]) {
                    result[0]=map[searchvalue-min]-1;
                    result[1]=i;
                    free(map);
                    return result;
                }
            }
        }
        map[value-min]=i+1;
    }
    free(map);  
    free(result);  
    return NULL; 
}