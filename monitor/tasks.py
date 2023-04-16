import asyncio
from typing import List
from celery import shared_task
from .utils import scanner


@shared_task()
def site_pulse_checker(sites:List[str]) -> None:
    """checks http status of urls in sites list"""
    asyncio.run(scanner(sites))
