# 這是一個我在113資訊科技二專班的作業
<p>
    由於怕我在未來的某一天想要帶學生玩這個作業，但又忘記怎麼操作所以就來記錄一下吧！
</p>

> 如果不知道 padding oracle Attack 是什麼的話請自己google，又或是自己看pdf(超不負責任的啊) 

## Task 1: Getting Familiar with Padding
<p>
    就是去觀察 Padding 後的樣子～～並去思考為什麼 Padding 為什麼需要把空間補滿？？
</p>
    
## Task 2: Padding Oracle Attack (Level 1)
<p>
    在開始做任務前思考下我們應該要做什麼呢？
</p>

> 找到 C2 解密後的那的那塊（在文件中就可以了解了），接著透過根 C1 xor 就可以找到第二段的明文了＾＾

<p>
    那我們該如何去找到解密後的那塊(D2＝C2解密後的)呢？
</P>

> 想法一：透過暴力法把所有的 D2 找出來，然後觀察明文（但這只僅限於最後一段呢）

## Task 3: Padding Oracle Attack (Level 2)
<p>
    在任務2的練習後，我們想要將 Padding Oracle Attack 可以直接用程式來處理。因此可以根據 Padding 的方式來稍微的修改程式碼就好了～
</p>