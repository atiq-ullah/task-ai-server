import json
import time
import logging
from django.http import JsonResponse
from .helpers import (
    PromptType,
    PromptForm,
    validate_request,
    promptTypeMap,
    MessageForm,
    send_run_creation,
    client,
    PARSING_THREAD_ID,
    CAT_THREAD_ID
)
from . import celery


logger = logging.getLogger(__name__)


def post_prompt_handler(request):
    form = PromptForm(request.GET)
    
    if validate_request(form):
        return validate_request(request)
    
    prompt = form.cleaned_data['prompt']
    p_type = form.cleaned_data['p_type']

    logger.info(f'Prompt: {prompt}')
    logger.info(f'Prompt type: {p_type}')
    run_id = send_run_creation(p_type, prompt)
    periodically_check_run_status.delay(p_type, run.id)
    
    return JsonResponse(data={"run_id": run_id})

def get_prompt_handler(request):
    form = MessageForm(request.GET)
    
    if validate_request(form):
        return validate_request(request)
   
    p_type = form.cleaned_data['p_type']

    message_list = client.beta.threads.messages.list(
        thread_id=promptTypeMap[p_type]
    ).json()

    return JsonResponse(data={"messages": message_list})

@celery.task(soft_time_limit=30)
def periodically_check_run_status(p_type, run_id):
    while True:
        try:
            time.sleep(5)
            run = client.beta.threads.runs.retrieve(run_id, thread_id=promptTypeMap[p_type])   

            if run.status == "completed":
                last_message = client.beta.threads.messages.list(thread_id=promptTypeMap[p_type]).data[0].content[0]
                logger.info(last_message.text.value)
                break
            else:
                logger.info(f'Run status: {run.status}')
        except Exception as e:
            logger.error(f'An error occurred: {e}')
