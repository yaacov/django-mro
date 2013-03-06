from django_cron import CronJobBase, Schedule
from django.core.management import call_command

class ReadCounters(CronJobBase):
    RUN_EVERY_MINS = 60 * 6 # every 6 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'mro_system_read_counters'    # a unique code

    def do(self):
        # This will be executed every 6 hours
        call_command('read_system_counter', interactive = False)

class CheckMaintenance(CronJobBase):
    RUN_EVERY_MINS = 60 * 12 # every 12 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'mro_system_check_maintenance'    # a unique code

    def do(self):
        # This will be executed every 12 hours
        call_command('check_maintenance_schedual', interactive = False)
