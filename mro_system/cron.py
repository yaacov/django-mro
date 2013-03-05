from django_cron import cronScheduler, Job

from django.core.management import call_command

class ReadCounters(Job):
        """
                Cron Job that checks counter readings
        """

        # run every 6 hours
        run_every = 60 * 60 * 6
                
        def job(self):
                # This will be executed every 6 hours
                call_command('read_system_counter', interactive = False)

class CheckMaintenance(Job):
        """
                Cron Job that create new work orders if needed
        """

        # run every 12 hours
        run_every = 60 * 60 * 12
                
        def job(self):
                # This will be executed every 12 hours
                call_command('check_maintenance_schedual', interactive = False)

cronScheduler.register(ReadCounters)
cronScheduler.register(CheckMaintenance)
