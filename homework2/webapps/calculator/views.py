from django.shortcuts import render

# Create your views here.
num = ["1","2","3","4","5","6","7","8","9","0"]
opt = ["+","-","*","/"]
eql = "="
clr = "C"

def home(request):
	if request.method == "GET":
		context = {"display": 0, "preval": 0, "preopt": "+", "curval": 0, "error": 0}
		return render(request, "calculator/calculator.html", context)
	if request.method == "POST":
		if clr in request.POST.keys():
			context = init()
		elif request.POST["error"] == "1":
			context = error()
		else:
			for key in request.POST.keys():
				if key in num:
					context = updateVal(request, key)
				elif key in opt:
					context = updateOpt(request, key)
				elif key == eql:
					context = computeResult(request, key)
		return render(request, "calculator/calculator.html", context)

def updateVal(request, val):
	preVal = request.POST["preval"]
	curVal = request.POST["curval"]
	preOpt = request.POST["preopt"]

	if curVal == "0":
		curVal = val
	elif len(curVal) < 19: # python int -9223372036854775808 ~ 9223372036854775807
		curVal += val
	
	# context = request.POST.copy()
	# context.update({"curval": curVal, "display": curVal});
	context = {"preval": preVal, "curval": curVal, "preopt": preOpt, "display": curVal}
	return context

def updateOpt(request, key):
	preVal = request.POST["preval"]
	curVal = request.POST["curval"]
	preOpt = request.POST["preopt"]
	
	preVal = compute(preVal, curVal, preOpt)
	if preVal == "Error":
		context = error();
		# context = request.POST.copy()
		# context.update({"error" : 1, "display" : "Error"})		
	else:	
		curVal = 0
		preOpt = key	

		# context = request.POST.copy()
		# context.update({"preval": preVal, "curval": curVal, "preopt": preOpt, "display": preVal});
		context = {"preval": preVal, "curval": curVal, "preopt": preOpt, "display": preVal}
	return context;	

def computeResult(request, key):
	preVal = request.POST["preval"]
	curVal = request.POST["curval"]
	preOpt = request.POST["preopt"]	

	res = compute(preVal, curVal, preOpt)
	if res == "Error":
		context = error();
		# context = request.POST.copy()
		# context.update({"error" : 1, "display" : "Error"})
	else:
		preVal = 0
		curVal = 0
		preOpt = "+"

		# context = request.POST.copy()
		# context.update({"preval": preVal, "curval": curVal, "preopt": preOpt, "display": res});
		context = {"preval": preVal, "curval": curVal, "preopt": preOpt, "display": res}
	return context;

def compute(preVal, curVal, opt):
	res = 0
	if opt == "+":
		res = int(preVal) + int(curVal)
	elif opt == "-":
		res = int(preVal) - int(curVal)
	elif opt == "*":
		res = int(preVal) * int(curVal)
	elif opt == "/":
		try:
			res = int(preVal) / int(curVal)
		except ZeroDivisionError:
			res = "Error"
	return res
	
def init():
	return {"display": 0, "preval": 0, "preopt": "+", "curval": 0, "error": 0}

def error():
	return {"error" : 1, "display" : "Error"}



