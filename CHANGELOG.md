# Changelog
## [V1.5](https://github.com/ncu-psl/BigO-Calc/releases/tag/v1.5)
[Full Changelog](https://github.com/chunlin-pan/DYSTA/compare/chunlin-pan:v1.4...v1.5)
1. 修正無法分析 a ** b (a的b次方)的語法。
2. 支援各種置於 For statemnt 中 itertation 節點的 function call
    ```py=
    import math
    def module16():
        result = []
        for i in dir(math):
            if 'exam' in i:
                result.append(i)
        print(result)
    ```
    這樣的程式經過時間複雜度分析後可以得到
    ```json=
    {
        "compilation node": "O(1)",
        "module16": "O(#dir(math))"
    }
    ```
    輸出結果為了避免跟計算dir(math)所需的時間複雜度搞混，
    在 function 前面加一個#表示這個 function output 的 list 或是 tuple 的大小。

    可支援的 function call 以 EBNF 來表示
    ```
    FUNCALL ::= CALL | ATTRIBUTE ;

    CALL ::= NAME , '(' , ARGS , ')' ;

    ARGS ::= ARG , { ',' , ARG } ;

    ARG ::= CALL | NAME | ATTRIBUTE ;

    ATTRIBUTE ::= VALUE , '.' , ATTR ;

    VALUE ::= NAME | ATTRIBUTE ;

    ATTR ::= CALL | NAME ;

    NAME ::= id ;

    // ::= 表示 左式可被展成右式
    // {} 內的元素可以可以省略或重複出現
    // | 表示 或
    ```
