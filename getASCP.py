# -*- coding:utf-8 -*-

import hashlib
import time
import math

'''
头条号主主页历史文章翻页请求参数AS、CP的获取
'''

def get_ASCP():
    t = int(math.floor(time.time()))
    e = hex(t).upper()[2:]
    m = hashlib.md5()
    m.update(str(t).encode(encoding='utf-8'))
    i = m.hexdigest().upper()

    if len(e) != 8:
        AS = '479BB4B7254C150'
        CP = '7E0AC8874BB0985'
        return AS,CP
    n = i[0:5]
    a = i[-5:]
    s = ''
    r = ''
    for o in range(5):
        s += n[o] + e[o]
        r += e[o + 3] + a[o]

    AS = 'A1' + s + e[-3:]
    CP = e[0:3] + r + 'E1'
    return AS,CP

if __name__ == "__main__":
    print(get_ASCP())
    print(get_ASCP()[0])
    print(get_ASCP()[1])

 '''
 头条号主主页历史文章翻页请求参数AS、CP的原JS代码
 i.getHoney = function() {
	var t=Math.floor((new Date).getTime()/1e3),
	i=t.toString(16).toUpperCase(),
	e=md5(t).toString().toUpperCase();
	if(8!=i.length)
		return{
			as:"479BB4B7254C150",
			cp:"7E0AC8874BB0985"
		};
	for(var s=e.slice(0,5),o=e.slice(-5),n="",a=0;5>a;a++)
		n+=s[a]+i[a];
	for(var l="",r=0;5>r;r++)
		l+=i[r+3]+o[r];
	return{
		as:"A1"+n+i.slice(-3),
		cp:i.slice(0,3)+l+"E1"
	}
},

function o(){
	var t,i=ascp.getHoney(),
	e="";
	return window.TAC&&(e=TAC.sign(userInfo.id+""+c.params.max_behot_time)),
	t=_.extend({},c.params,{
		as:i.as,cp:i.cp,_signature:e})
}
'''
