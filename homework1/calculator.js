var preVal=0;
var curVal=0;
var preOpt="+";

var numbers = document.getElementsByClassName("number");
var operators = document.getElementsByClassName("operator");
var result = document.getElementById("=");

function load() {
	for(n in numbers) {
		numbers[n].onclick = updateVal;
	}

	for(o in operators) {
		operators[o].onclick = updateOpt;
	}

	result.onclick = computeResult;
}

function updateVal() {
	if (curVal == 0) {
		curVal = this.id;
	}
	else if (curVal.length < 10){
		curVal += this.id;
	}
	document.getElementById("display").value = curVal;
}

function updateOpt() {
	compute();
	preOpt = this.id;
	curVal = 0;
}

function computeResult() {
	compute();
	preVal = 0;
	curVal = 0;
	preOpt = "+";

}

function compute() {
	switch(preOpt) {
		case "+":
			preVal = parseInt(preVal) + parseInt(curVal);
			break;
		case "-":
			preVal = parseInt(preVal) - parseInt(curVal);
			break;
		case "*":
			preVal = parseInt(preVal) * parseInt(curVal);
			break;
		case "/":
			if(curVal == 0) {
				divError();
				return;
			}
			preVal = Math.floor(parseInt(preVal) / parseInt(curVal));
			break;
	}
	document.getElementById("display").value = preVal;

}

function divError() {
	document.getElementById("display").value = "Error";
	var buttons = document.getElementsByTagName("button");
	for (b in buttons) {
		buttons[b].onclick = null;
	}
}