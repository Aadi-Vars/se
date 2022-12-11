from django.shortcuts import render
from django.http import HttpResponse
from .models import question_object
from pathlib import Path
import os
import time
BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.
def home(request):
	global avai_exam,exam
	if request.POST:
		pathy=os.path.join(BASE_DIR,"static/"+request.POST["exam"])
		avai_paper=os.listdir(pathy)
		
		exam=request.POST["exam"]
		
		return render(request,"web.html",{"object2":avai_paper,'object':avai_exam,"exam":exam})
		
		
	else:
		
		pathy=os.path.join(BASE_DIR,"static/")
		avai_exam=os.listdir(pathy)
		avai_exam.remove("img")

		return render(request,'web.html',{'object':avai_exam})
	
def instr(request):
	
	global paper
	try:
		paper=request.POST['paper']
	except:
		pass
	return render(request,'instr.html')
	
def other_imp_instr(request):
	global avai_lang,exam
	pathy=os.path.join(BASE_DIR,"static/"+exam+"/"+paper)
	avai_lang=os.listdir(pathy)
	
	return render(request,'other_imp_instr.html',{"opt_hidden":"True","check_hidden":"True","avai_lang":avai_lang})
	
# showing paper first time
def paper_1(request):
		global final_index,seen_question,result,start_time,language,avai_lang
		final_index=-7
		start_time=time.time()
		seen_question=[]
		result={}
		if "opt" in request.POST:
			language=request.POST["opt"]
		else:
			return render(request,'other_imp_instr.html',{"opt_hidden":"False","check_hidden":"True","avai_lang":avai_lang})
			
		if "check" in request.POST:
			pass
		else:
			return render(request,'other_imp_instr.html',{"opt_hidden":"True","check_hidden":"False","avai_lang":avai_lang})
		
		return ques_print(request)

# showing question
def ques_print(request):
		global paper,language,exam
		f=open(os.path.join(BASE_DIR,"static/"+exam+"/"+paper+"/"+language+"/"+"txt/"+paper+".txt"),"r")
		data=f.readlines()
		f.close()
		for i in range(len(data)):
			data[i]=data[i].rstrip("\n")
		
		global final_index,question
		if final_index+7<len(data):
			
			final_index+=7
			question=question_object()
			
			question.instr=data[final_index]
			question.ques=data[final_index+1]
			question.a=data[final_index+2]
			question.b=data[final_index+3]
			question.c=data[final_index+4]
			question.d=data[final_index+5]
			if data[final_index+6].startswith("[") and data[final_index+6].endswith("]"):
				data[final_index+6]= data[final_index+6].lstrip("[")
				data[final_index+6]= data[final_index+6].rstrip("]")
				question.corr_opt=data[final_index+6].split(",")
			
			else:
				question.corr_opt=data[final_index+6]
			
		else:
			final_index=0
			question=question_object()
			question.instr=data[final_index]
			question.ques=data[final_index+1]
			question.a=data[final_index+2]
			question.b=data[final_index+3]
			question.c=data[final_index+4]
			question.d=data[final_index+5]
			
			if data[final_index+6].startswith("[") and data[final_index+6].endswith("]"):
				data[final_index+6]= data[final_index+6].lstrip("[")
				data[final_index+6]= data[final_index+6].rstrip("]")
				question.corr_opt=data[final_index+6].split(",")
			
			else:
				question.corr_opt=data[final_index+6]
			
		if question.a=="integer":
			question.type="integer"
		elif type(question.corr_opt)==list:
			question.type="multi"
		else:
			question.type="only_one"
		
		global seen_question,result
		if question.ques in seen_question:
			#sending selected value
			
			question.select_val=result[question.ques]
			
			
		
		return render(request,'paper.html',{'object':question,'exam':exam,'paper':paper})

# Next & save
def paper(request):
	
	global seen_question,result,question
	# marking question as seen
	seen_question.append(question.ques)
	if question.a=="integer":
		if 'ans2' in request.POST:
			result[question.ques]=request.POST['ans2']
		else:
			result[question.ques]='None'
	elif question.type=="only_one":
		if 'ans' in request.POST:
			result[question.ques]=request.POST['ans']
		else:
			result[question.ques]='None'
	else:
		ans=[]
		if 'ans1' in request.POST:
			ans.append(request.POST['ans1'])
		if 'ans2' in request.POST:
			ans.append(request.POST['ans2'])
		if 'ans3' in request.POST:
			ans.append(request.POST['ans3'])
		if 'ans4' in request.POST:
			ans.append(request.POST['ans4'])
		if len(ans)==0:
			ans.append("None")
		result[question.ques]=ans
		
	return ques_print(request)
	
# clear reaponses
def clear(request):
	global question,final_index,seen_question,result
	
	final_index=final_index-7
	result[question.ques]='None'
	question.select_val='None'
	
	return ques_print(request)


# submitting the paper
def submit(request):
	global review_ques,result,question,result,paper,end_time,start_time,language
	end_time=time.time()
	spend_time=end_time-start_time
	spend_time=spend_time/60
	spend_time=round(spend_time,4)
	
	
	f=open(os.path.join(BASE_DIR,"static/"+exam+"/"+paper+"/"+language+"/"+"txt/"+paper+".txt"),"r")
	print(f)
	data=f.readlines()
	f.close()
	
	for i in range(len(data)):
		data[i]=data[i].rstrip("\n")
		
	listy=[]
	for i in range(0,len(data),7):
			
		question=question_object()
		question.instr=data[i]
		question.ques=data[i+1]
		question.a=data[i+2]
		question.b=data[i+3]
		question.c=data[i+4]
		question.d=data[i+5]
		
		# getting selected value
		if question.ques in result:
			question.select_val=result[question.ques]
		else:
			question.select_val="None"
			
		
		#getting correct value
		if data[i+6].startswith("[") and data[i+6].endswith("]"):
			data[i+6]= data[i+6].lstrip("[")
			data[i+6]= data[i+6].rstrip("]")
			question.corr_opt=data[i+6].split(",")
			
		else:
			question.corr_opt=data[i+6]
			
			
		if question.a=="integer":
			question.type="integer"
		elif type(question.corr_opt)==list:
			question.type="multi"
		else:
			question.type="only_one"
		listy.append(question)
	

	
	return render(request,"submit.html",{'object':listy,'time':spend_time})
	
	
# marking for review
def review(request):
	
	global review_ques,question
	review_ques=[]
	review_ques.append(question.ques)
	
	return ques_print(request)