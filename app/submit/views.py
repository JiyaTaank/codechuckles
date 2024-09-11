from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from submit.forms import CodeSubmissionForm
from home.models import question
import os
import subprocess
from subprocess import TimeoutExpired
import uuid
from pathlib import Path

'''def pre_run(request,question_id):
    question_detail = get_object_or_404 (question, id=question_id)

    output=" "
    status_message=""

    if request.method == 'POST':
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission= form.save(commit=False)
            submission.question=question_detail
            submission.user=request.user
            
            #print(submission.language)
            #print(submission.code)
            output=run_code(
                submission.language,submission.code,submission.input_data
            )
            submission.output_data=output
            submission.save()
            return render(request,"question_detail.html",{"submission":submission,"output":output,"status":submission.status})
    else:
        form = CodeSubmissionForm()
        
    return render(request,"question_detail.html",{"form":form,"question":question_detail})'''


def run_code(language,code,input_data,time_limit):
    
    input_data=input_data.replace('\r\n','\n')
    
    project_path=Path(settings.BASE_DIR)
    directories=["codes","inputs","outputs"]

    for directory in directories:
        dir_path= project_path/directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True,exist_ok=True)

    codes_dir=project_path/ "codes"
    inputs_dir=project_path/ "inputs"
    outputs_dir=project_path/ "outputs"

    unique=str(uuid.uuid4())

    code_file_name=f"{unique}.{language}"
    input_file_name=f"{unique}.txt"
    output_file_name=f"{unique}.txt"

    code_file_path=codes_dir/code_file_name
    input_file_path=inputs_dir/input_file_name
    output_file_path=outputs_dir/output_file_name

    with open(code_file_path,"w") as code_file:
        code_file.write(code)
    with open(input_file_path,"w") as input_file:
        input_file.write(input_data)
    with open(output_file_path,"w") as output_file:
        pass

        try:
           if language=="cpp":
              executable_path=codes_dir/unique
              compile_result=subprocess.run(
                ["g++",str(code_file_path),"-o",str(executable_path)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                
            )
            
            
              if compile_result.returncode == 0:
                with open(input_file_path,"r") as input_file:
                    with open(output_file_path,"w") as output_file:
                        run_result=subprocess.run(
                            [str(executable_path)],
                            stdin=input_file,
                            stdout=output_file,
                            stderr=subprocess.PIPE,
                            timeout=time_limit
                        )
                        if run_result.returncode != 0:
                            return f"Program exited with return code {run_result.returncode}. Output:\n{run_result.stderr.decode()}"  
              else:
                return compile_result.stderr.decode()
        
           elif language =="py":
            with open(input_file_path,"r") as input_file:
                with open(output_file_path,"w") as output_file:
                    run_result=subprocess.run(
                        ["python",str(code_file_path)],
                        stdin=input_file,
                        stdout=output_file,
                        stderr=subprocess.PIPE,
                        timeout=time_limit
                    )
                    
    
                    if run_result.returncode != 0:
                        return  f"Program exited with return code {run_result.returncode}. Error:\n{run_result.stderr.decode()}"
                    
    
           elif language=="c":
            executable_path=codes_dir/unique
            compile_result=subprocess.run(
                ["gcc",str(code_file_path),"-o",str(executable_path)],stdout=subprocess.PIPE,stderr=subprocess.PIPE
            )
            
            
            if compile_result.returncode == 0:
                with open(input_file_path,"r") as input_file:
                    with open(output_file_path,"w") as output_file:
                        run_result=subprocess.run(
                            [str(executable_path)],
                            stdin=input_file,
                            stdout=output_file,
                            stderr=subprocess.PIPE,
                            timeout=time_limit,
                            
                        )
                        if run_result.returncode != 0:
                           return f"Program exited with return code {run_result.returncode}. Output:\n{run_result.stderr.decode()}"
            else:
              return compile_result.stderr.decode()
            
        except TimeoutExpired:
           output_data="Time Limit Exceeded"
           return output_data

    with open(output_file_path,"r") as output_file:
        output_data=output_file.read()
    return output_data 
