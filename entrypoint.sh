#!/bin/sh
celery -A tasks worker --pool=solo -Q kitchen -l info
