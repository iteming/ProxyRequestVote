import time
import multiprocessing
from examples import usage
from setting import CYCLE_TESTER, ENABLE_TESTER, IS_WINDOWS
from loguru import logger


if IS_WINDOWS:
    multiprocessing.freeze_support()

tester_process, getter_process, server_process = None, None, None


class Scheduler():
    """
    scheduler
    """

    def run_tester(self, cycle=CYCLE_TESTER):
        """
        run tester
        """
        if not ENABLE_TESTER:
            logger.info('tester not enabled, exit')
            return
        loop = 0

        global int_count
        int_count = 0
        while True:
            logger.debug(f'tester loop {loop} start...')
            int_count = usage.main(int_count)
            loop += 1
            time.sleep(cycle)

    def run(self):
        global tester_process
        try:
            logger.info('starting xxxxx...')

            tester_process = multiprocessing.Process(target=self.run_tester)
            logger.info(f'starting tester, pid {tester_process.pid}...')
            tester_process.start()

            tester_process.join()
        except KeyboardInterrupt:
            logger.info('received keyboard interrupt signal')
            tester_process.terminate()
        finally:
            # must call join method before calling is_alive
            tester_process.join()
            logger.info(f'tester is {"alive" if tester_process.is_alive() else "dead"}')
            logger.info('proxy terminated')

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
