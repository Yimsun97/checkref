@echo off
REM set the arguments for the script
set api_provider=aliyun
set model=deepseek-v3
set num_per_request=50
set REF_PATH=<path_to_your_reference_list>
set INPUT_FILE=%REF_PATH%\<your_reference_list>.csv
set OUTPUT_PATH=%REF_PATH%\<your_reference_list>_

REM start the script
echo Start
echo api_provider: %api_provider%, model: %model%, num_per_request: %num_per_request%
echo REF_PATH: %REF_PATH%

python main.py --api_provider %api_provider% --model %model% --input_file %INPUT_FILE% --output_path %OUTPUT_PATH% --num_per_request %num_per_request%

echo Done
pause 