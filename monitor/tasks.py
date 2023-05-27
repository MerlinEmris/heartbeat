import asyncio
from typing import List, Dict
from celery import shared_task
from .utils import scanner


@shared_task()
def site_pulse_checker(sites:List[Dict[str,str]],chanel_name:str) -> None:
    """checks http status of urls in sites list"""
    asyncio.run(scanner(sites,chanel_name))

