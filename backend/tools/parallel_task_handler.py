import multiprocessing
import signal
import time

class ParallelTaskHandler:
    def __init__(self, task_create_fn, process_fn, post_process_fn = lambda arr: arr, num_processes = multiprocessing.cpu_count(), safe_mode=True):
        # The initializer argument tells the workers to ignore the 'Ctrl+C' signal,
        # to avoid raising any exceptions in the worker processes
        self.num_processes = num_processes
        self.task_create_fn = task_create_fn
        self.process_fn = process_fn
        self.post_process_fn = post_process_fn
        self.safe_mode = safe_mode
        self.pool = multiprocessing.Pool(
            processes = self.num_processes,
            initializer = lambda: signal.signal(signal.SIGINT, signal.SIG_IGN)
        )


    def process_items(self, items):
        # Generate a list of n-tuple params for the process workers to parse
        task_params = self.task_create_fn(items)
        num_tasks = len(task_params)

        print('\nProcessing {0} tasks with {1} processors...'.format(num_tasks, self.num_processes))

        try:
            raw_result = self.pool.map_async(self.process_fn, task_params, chunksize=num_tasks // self.num_processes)

            # This loop awaits the result by using a low-resource usage loop
            while not raw_result.ready():
                time.sleep(0.01)
        except KeyboardInterrupt:
            # If the user wants to cancel, gracefully shut down
            self.pool.terminate()

            if self.safe_mode:
                self.pool.close()

            # Join all the processes to properly clean up
            self.pool.join()

            # Raise the error again to acknowledge the user wanting to cancel the operation
            raise KeyboardInterrupt
        except ValueError:
            print('Pool is already closed! Cancelling current job...')

        final_result = raw_result.get()
        return self.post_process_fn(final_result)

    # Closes the pool to prevent more tasks from being processed and join the existing processes
    def cleanup(self):
        self.pool.close()
        self.pool.join()