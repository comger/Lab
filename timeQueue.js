function TimeQueue() {
	this.queue = []; 
	this.waitid = 0;
	this.timeouthandle = null;
	this.id = 1;
}

TimeQueue.prototype.add = function(func,timeout){
	function sortby(a,b){ return a.timeout > b.timeout; }
	//增加一个任务
	//func调用的函数
	//timeout: 毫秒数
	this.queue.push( {id:this.id,func:func,timeout:timeout+(new Date()).valueOf()} );
	this.id += 1;
	this.queue.sort(sortby);
}

function waitQueue(obj){
	return function(){
		obj.waitid = 0;	
		obj.timeouthandle = null;
		obj.schedule();
	}
}

TimeQueue.prototype.schedule = function(){
	/*场景有如下几种:
		1. 空任务
		2. 有一个
		3. 有一个，并且前一个在Timeout的
	*/
	if (this.queue.length < 1) return; //接下去不用再shedule
	if (this.waitid > 0){ //已经调用了setTimeout了的.
		//已经设定wait的了,但是要看一下是否新加入的要求更快执行
		if (this.queue[0].id == this.waitid) return;
		//需要修改waitid的了.
		var now = (new Date()).valueOf();
		this.waitid = this.queue[0].id;
		var	left = this.queue[0].timeout - now;
		if (left < 2000) left = 2000; //强制2秒后运行.
		if (this.timeouthandle) clearTimeout(this.timeouthandle); //关闭上一次的Timeout.
		this.timeouthandle = setTimeout(waitQueue(this),left); //2秒后执行
		return;
	}
	//新的任务优先级更好，需要修改settimeout的值了.	
	var now = (new Date()).valueOf();
	var i = this.queue[0];
	if (i.timeout <= now) {
		this.queue.shift();
		i.func(); //运行
	}
	if (this.queue.length < 1) return; //接下去不用了
	var now = (new Date()).valueOf();
	var	left = this.queue[0].timeout - now;
	if (left < 2000) left = 2000; //强制2秒后运行.
	this.waitid = this.queue[0].id; //等待的ID
	this.timeouthandle = setTimeout(waitQueue(this),left); //2秒后执行
}
