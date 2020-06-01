static int lengthOfLongestSubstring(char s)
{
    int offset[128];
    int max_len = 0;
    int len = 0;
    int index = 0;

    memset(offset, 0xff, sizeof(offset));
    // int s_len = len(s); //還沒做出assign function call
    for (int i = 0; i < s_len; i++) {
        offset_Si = offset[s[i]];
        if (offset_Si == -1) {
            len++;
        } else {
            int index_minus_offest_Si = index - offset_Si;
            if (index_minus_offest_Si > len) {
                len++;
            } else {
	        len = index - offset_Si;
            }
        }
        if (len > max_len) {
            max_len = len;
        }
        offset_Si = index;
        index++;
    }

    return max_len;
}
